# provide/foundation/errors/runtime.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any

from provide.foundation.errors.base import FoundationError

"""Runtime and process execution exceptions."""
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class RuntimeError(FoundationError):
    """Raised for runtime operational errors.

    Args:
        message: Error message describing the runtime issue.
        operation: Optional operation that failed.
        retry_possible: Whether the operation can be retried.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise RuntimeError("Process failed")
        >>> raise RuntimeError("Lock timeout", operation="acquire_lock", retry_possible=True)

    """

    def xǁRuntimeErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        operation: str | None = None,
        retry_possible: bool = False,
        **kwargs: Any,
    ) -> None:
        if operation:
            kwargs.setdefault("context", {})["runtime.operation"] = operation
        kwargs.setdefault("context", {})["runtime.retry_possible"] = retry_possible
        super().__init__(message, **kwargs)

    def xǁRuntimeErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        operation: str | None = None,
        retry_possible: bool = True,
        **kwargs: Any,
    ) -> None:
        if operation:
            kwargs.setdefault("context", {})["runtime.operation"] = operation
        kwargs.setdefault("context", {})["runtime.retry_possible"] = retry_possible
        super().__init__(message, **kwargs)

    def xǁRuntimeErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        operation: str | None = None,
        retry_possible: bool = False,
        **kwargs: Any,
    ) -> None:
        if operation:
            kwargs.setdefault("context", {})["runtime.operation"] = None
        kwargs.setdefault("context", {})["runtime.retry_possible"] = retry_possible
        super().__init__(message, **kwargs)

    def xǁRuntimeErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        operation: str | None = None,
        retry_possible: bool = False,
        **kwargs: Any,
    ) -> None:
        if operation:
            kwargs.setdefault(None, {})["runtime.operation"] = operation
        kwargs.setdefault("context", {})["runtime.retry_possible"] = retry_possible
        super().__init__(message, **kwargs)

    def xǁRuntimeErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        operation: str | None = None,
        retry_possible: bool = False,
        **kwargs: Any,
    ) -> None:
        if operation:
            kwargs.setdefault("context", None)["runtime.operation"] = operation
        kwargs.setdefault("context", {})["runtime.retry_possible"] = retry_possible
        super().__init__(message, **kwargs)

    def xǁRuntimeErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        operation: str | None = None,
        retry_possible: bool = False,
        **kwargs: Any,
    ) -> None:
        if operation:
            kwargs.setdefault({})["runtime.operation"] = operation
        kwargs.setdefault("context", {})["runtime.retry_possible"] = retry_possible
        super().__init__(message, **kwargs)

    def xǁRuntimeErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        operation: str | None = None,
        retry_possible: bool = False,
        **kwargs: Any,
    ) -> None:
        if operation:
            kwargs.setdefault("context", )["runtime.operation"] = operation
        kwargs.setdefault("context", {})["runtime.retry_possible"] = retry_possible
        super().__init__(message, **kwargs)

    def xǁRuntimeErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        operation: str | None = None,
        retry_possible: bool = False,
        **kwargs: Any,
    ) -> None:
        if operation:
            kwargs.setdefault("XXcontextXX", {})["runtime.operation"] = operation
        kwargs.setdefault("context", {})["runtime.retry_possible"] = retry_possible
        super().__init__(message, **kwargs)

    def xǁRuntimeErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        operation: str | None = None,
        retry_possible: bool = False,
        **kwargs: Any,
    ) -> None:
        if operation:
            kwargs.setdefault("CONTEXT", {})["runtime.operation"] = operation
        kwargs.setdefault("context", {})["runtime.retry_possible"] = retry_possible
        super().__init__(message, **kwargs)

    def xǁRuntimeErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        operation: str | None = None,
        retry_possible: bool = False,
        **kwargs: Any,
    ) -> None:
        if operation:
            kwargs.setdefault("context", {})["XXruntime.operationXX"] = operation
        kwargs.setdefault("context", {})["runtime.retry_possible"] = retry_possible
        super().__init__(message, **kwargs)

    def xǁRuntimeErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        operation: str | None = None,
        retry_possible: bool = False,
        **kwargs: Any,
    ) -> None:
        if operation:
            kwargs.setdefault("context", {})["RUNTIME.OPERATION"] = operation
        kwargs.setdefault("context", {})["runtime.retry_possible"] = retry_possible
        super().__init__(message, **kwargs)

    def xǁRuntimeErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        operation: str | None = None,
        retry_possible: bool = False,
        **kwargs: Any,
    ) -> None:
        if operation:
            kwargs.setdefault("context", {})["runtime.operation"] = operation
        kwargs.setdefault("context", {})["runtime.retry_possible"] = None
        super().__init__(message, **kwargs)

    def xǁRuntimeErrorǁ__init____mutmut_12(
        self,
        message: str,
        *,
        operation: str | None = None,
        retry_possible: bool = False,
        **kwargs: Any,
    ) -> None:
        if operation:
            kwargs.setdefault("context", {})["runtime.operation"] = operation
        kwargs.setdefault(None, {})["runtime.retry_possible"] = retry_possible
        super().__init__(message, **kwargs)

    def xǁRuntimeErrorǁ__init____mutmut_13(
        self,
        message: str,
        *,
        operation: str | None = None,
        retry_possible: bool = False,
        **kwargs: Any,
    ) -> None:
        if operation:
            kwargs.setdefault("context", {})["runtime.operation"] = operation
        kwargs.setdefault("context", None)["runtime.retry_possible"] = retry_possible
        super().__init__(message, **kwargs)

    def xǁRuntimeErrorǁ__init____mutmut_14(
        self,
        message: str,
        *,
        operation: str | None = None,
        retry_possible: bool = False,
        **kwargs: Any,
    ) -> None:
        if operation:
            kwargs.setdefault("context", {})["runtime.operation"] = operation
        kwargs.setdefault({})["runtime.retry_possible"] = retry_possible
        super().__init__(message, **kwargs)

    def xǁRuntimeErrorǁ__init____mutmut_15(
        self,
        message: str,
        *,
        operation: str | None = None,
        retry_possible: bool = False,
        **kwargs: Any,
    ) -> None:
        if operation:
            kwargs.setdefault("context", {})["runtime.operation"] = operation
        kwargs.setdefault("context", )["runtime.retry_possible"] = retry_possible
        super().__init__(message, **kwargs)

    def xǁRuntimeErrorǁ__init____mutmut_16(
        self,
        message: str,
        *,
        operation: str | None = None,
        retry_possible: bool = False,
        **kwargs: Any,
    ) -> None:
        if operation:
            kwargs.setdefault("context", {})["runtime.operation"] = operation
        kwargs.setdefault("XXcontextXX", {})["runtime.retry_possible"] = retry_possible
        super().__init__(message, **kwargs)

    def xǁRuntimeErrorǁ__init____mutmut_17(
        self,
        message: str,
        *,
        operation: str | None = None,
        retry_possible: bool = False,
        **kwargs: Any,
    ) -> None:
        if operation:
            kwargs.setdefault("context", {})["runtime.operation"] = operation
        kwargs.setdefault("CONTEXT", {})["runtime.retry_possible"] = retry_possible
        super().__init__(message, **kwargs)

    def xǁRuntimeErrorǁ__init____mutmut_18(
        self,
        message: str,
        *,
        operation: str | None = None,
        retry_possible: bool = False,
        **kwargs: Any,
    ) -> None:
        if operation:
            kwargs.setdefault("context", {})["runtime.operation"] = operation
        kwargs.setdefault("context", {})["XXruntime.retry_possibleXX"] = retry_possible
        super().__init__(message, **kwargs)

    def xǁRuntimeErrorǁ__init____mutmut_19(
        self,
        message: str,
        *,
        operation: str | None = None,
        retry_possible: bool = False,
        **kwargs: Any,
    ) -> None:
        if operation:
            kwargs.setdefault("context", {})["runtime.operation"] = operation
        kwargs.setdefault("context", {})["RUNTIME.RETRY_POSSIBLE"] = retry_possible
        super().__init__(message, **kwargs)

    def xǁRuntimeErrorǁ__init____mutmut_20(
        self,
        message: str,
        *,
        operation: str | None = None,
        retry_possible: bool = False,
        **kwargs: Any,
    ) -> None:
        if operation:
            kwargs.setdefault("context", {})["runtime.operation"] = operation
        kwargs.setdefault("context", {})["runtime.retry_possible"] = retry_possible
        super().__init__(None, **kwargs)

    def xǁRuntimeErrorǁ__init____mutmut_21(
        self,
        message: str,
        *,
        operation: str | None = None,
        retry_possible: bool = False,
        **kwargs: Any,
    ) -> None:
        if operation:
            kwargs.setdefault("context", {})["runtime.operation"] = operation
        kwargs.setdefault("context", {})["runtime.retry_possible"] = retry_possible
        super().__init__(**kwargs)

    def xǁRuntimeErrorǁ__init____mutmut_22(
        self,
        message: str,
        *,
        operation: str | None = None,
        retry_possible: bool = False,
        **kwargs: Any,
    ) -> None:
        if operation:
            kwargs.setdefault("context", {})["runtime.operation"] = operation
        kwargs.setdefault("context", {})["runtime.retry_possible"] = retry_possible
        super().__init__(message, )
    
    xǁRuntimeErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRuntimeErrorǁ__init____mutmut_1': xǁRuntimeErrorǁ__init____mutmut_1, 
        'xǁRuntimeErrorǁ__init____mutmut_2': xǁRuntimeErrorǁ__init____mutmut_2, 
        'xǁRuntimeErrorǁ__init____mutmut_3': xǁRuntimeErrorǁ__init____mutmut_3, 
        'xǁRuntimeErrorǁ__init____mutmut_4': xǁRuntimeErrorǁ__init____mutmut_4, 
        'xǁRuntimeErrorǁ__init____mutmut_5': xǁRuntimeErrorǁ__init____mutmut_5, 
        'xǁRuntimeErrorǁ__init____mutmut_6': xǁRuntimeErrorǁ__init____mutmut_6, 
        'xǁRuntimeErrorǁ__init____mutmut_7': xǁRuntimeErrorǁ__init____mutmut_7, 
        'xǁRuntimeErrorǁ__init____mutmut_8': xǁRuntimeErrorǁ__init____mutmut_8, 
        'xǁRuntimeErrorǁ__init____mutmut_9': xǁRuntimeErrorǁ__init____mutmut_9, 
        'xǁRuntimeErrorǁ__init____mutmut_10': xǁRuntimeErrorǁ__init____mutmut_10, 
        'xǁRuntimeErrorǁ__init____mutmut_11': xǁRuntimeErrorǁ__init____mutmut_11, 
        'xǁRuntimeErrorǁ__init____mutmut_12': xǁRuntimeErrorǁ__init____mutmut_12, 
        'xǁRuntimeErrorǁ__init____mutmut_13': xǁRuntimeErrorǁ__init____mutmut_13, 
        'xǁRuntimeErrorǁ__init____mutmut_14': xǁRuntimeErrorǁ__init____mutmut_14, 
        'xǁRuntimeErrorǁ__init____mutmut_15': xǁRuntimeErrorǁ__init____mutmut_15, 
        'xǁRuntimeErrorǁ__init____mutmut_16': xǁRuntimeErrorǁ__init____mutmut_16, 
        'xǁRuntimeErrorǁ__init____mutmut_17': xǁRuntimeErrorǁ__init____mutmut_17, 
        'xǁRuntimeErrorǁ__init____mutmut_18': xǁRuntimeErrorǁ__init____mutmut_18, 
        'xǁRuntimeErrorǁ__init____mutmut_19': xǁRuntimeErrorǁ__init____mutmut_19, 
        'xǁRuntimeErrorǁ__init____mutmut_20': xǁRuntimeErrorǁ__init____mutmut_20, 
        'xǁRuntimeErrorǁ__init____mutmut_21': xǁRuntimeErrorǁ__init____mutmut_21, 
        'xǁRuntimeErrorǁ__init____mutmut_22': xǁRuntimeErrorǁ__init____mutmut_22
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRuntimeErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁRuntimeErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁRuntimeErrorǁ__init____mutmut_orig)
    xǁRuntimeErrorǁ__init____mutmut_orig.__name__ = 'xǁRuntimeErrorǁ__init__'

    def xǁRuntimeErrorǁ_default_code__mutmut_orig(self) -> str:
        return "RUNTIME_ERROR"

    def xǁRuntimeErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXRUNTIME_ERRORXX"

    def xǁRuntimeErrorǁ_default_code__mutmut_2(self) -> str:
        return "runtime_error"
    
    xǁRuntimeErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRuntimeErrorǁ_default_code__mutmut_1': xǁRuntimeErrorǁ_default_code__mutmut_1, 
        'xǁRuntimeErrorǁ_default_code__mutmut_2': xǁRuntimeErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRuntimeErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁRuntimeErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁRuntimeErrorǁ_default_code__mutmut_orig)
    xǁRuntimeErrorǁ_default_code__mutmut_orig.__name__ = 'xǁRuntimeErrorǁ_default_code'


class StateError(FoundationError):
    """Raised when an operation is invalid for the current state.

    Args:
        message: Error message describing the state issue.
        current_state: Optional current state.
        expected_state: Optional expected state.
        transition: Optional attempted transition.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise StateError("Invalid state transition")
        >>> raise StateError("Not ready", current_state="initializing", expected_state="ready")

    """

    def xǁStateErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["state.transition"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["state.current"] = None
        if expected_state:
            kwargs.setdefault("context", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["state.transition"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault(None, {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["state.transition"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", None)["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["state.transition"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault({})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["state.transition"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", )["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["state.transition"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("XXcontextXX", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["state.transition"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("CONTEXT", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["state.transition"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["XXstate.currentXX"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["state.transition"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["STATE.CURRENT"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["state.transition"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["state.expected"] = None
        if transition:
            kwargs.setdefault("context", {})["state.transition"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault(None, {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["state.transition"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_12(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", None)["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["state.transition"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_13(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault({})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["state.transition"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_14(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", )["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["state.transition"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_15(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("XXcontextXX", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["state.transition"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_16(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("CONTEXT", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["state.transition"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_17(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["XXstate.expectedXX"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["state.transition"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_18(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["STATE.EXPECTED"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["state.transition"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_19(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["state.transition"] = None
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_20(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault(None, {})["state.transition"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_21(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", None)["state.transition"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_22(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault({})["state.transition"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_23(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", )["state.transition"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_24(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("XXcontextXX", {})["state.transition"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_25(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("CONTEXT", {})["state.transition"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_26(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["XXstate.transitionXX"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_27(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["STATE.TRANSITION"] = transition
        super().__init__(message, **kwargs)

    def xǁStateErrorǁ__init____mutmut_28(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["state.transition"] = transition
        super().__init__(None, **kwargs)

    def xǁStateErrorǁ__init____mutmut_29(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["state.transition"] = transition
        super().__init__(**kwargs)

    def xǁStateErrorǁ__init____mutmut_30(
        self,
        message: str,
        *,
        current_state: str | None = None,
        expected_state: str | None = None,
        transition: str | None = None,
        **kwargs: Any,
    ) -> None:
        if current_state:
            kwargs.setdefault("context", {})["state.current"] = current_state
        if expected_state:
            kwargs.setdefault("context", {})["state.expected"] = expected_state
        if transition:
            kwargs.setdefault("context", {})["state.transition"] = transition
        super().__init__(message, )
    
    xǁStateErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStateErrorǁ__init____mutmut_1': xǁStateErrorǁ__init____mutmut_1, 
        'xǁStateErrorǁ__init____mutmut_2': xǁStateErrorǁ__init____mutmut_2, 
        'xǁStateErrorǁ__init____mutmut_3': xǁStateErrorǁ__init____mutmut_3, 
        'xǁStateErrorǁ__init____mutmut_4': xǁStateErrorǁ__init____mutmut_4, 
        'xǁStateErrorǁ__init____mutmut_5': xǁStateErrorǁ__init____mutmut_5, 
        'xǁStateErrorǁ__init____mutmut_6': xǁStateErrorǁ__init____mutmut_6, 
        'xǁStateErrorǁ__init____mutmut_7': xǁStateErrorǁ__init____mutmut_7, 
        'xǁStateErrorǁ__init____mutmut_8': xǁStateErrorǁ__init____mutmut_8, 
        'xǁStateErrorǁ__init____mutmut_9': xǁStateErrorǁ__init____mutmut_9, 
        'xǁStateErrorǁ__init____mutmut_10': xǁStateErrorǁ__init____mutmut_10, 
        'xǁStateErrorǁ__init____mutmut_11': xǁStateErrorǁ__init____mutmut_11, 
        'xǁStateErrorǁ__init____mutmut_12': xǁStateErrorǁ__init____mutmut_12, 
        'xǁStateErrorǁ__init____mutmut_13': xǁStateErrorǁ__init____mutmut_13, 
        'xǁStateErrorǁ__init____mutmut_14': xǁStateErrorǁ__init____mutmut_14, 
        'xǁStateErrorǁ__init____mutmut_15': xǁStateErrorǁ__init____mutmut_15, 
        'xǁStateErrorǁ__init____mutmut_16': xǁStateErrorǁ__init____mutmut_16, 
        'xǁStateErrorǁ__init____mutmut_17': xǁStateErrorǁ__init____mutmut_17, 
        'xǁStateErrorǁ__init____mutmut_18': xǁStateErrorǁ__init____mutmut_18, 
        'xǁStateErrorǁ__init____mutmut_19': xǁStateErrorǁ__init____mutmut_19, 
        'xǁStateErrorǁ__init____mutmut_20': xǁStateErrorǁ__init____mutmut_20, 
        'xǁStateErrorǁ__init____mutmut_21': xǁStateErrorǁ__init____mutmut_21, 
        'xǁStateErrorǁ__init____mutmut_22': xǁStateErrorǁ__init____mutmut_22, 
        'xǁStateErrorǁ__init____mutmut_23': xǁStateErrorǁ__init____mutmut_23, 
        'xǁStateErrorǁ__init____mutmut_24': xǁStateErrorǁ__init____mutmut_24, 
        'xǁStateErrorǁ__init____mutmut_25': xǁStateErrorǁ__init____mutmut_25, 
        'xǁStateErrorǁ__init____mutmut_26': xǁStateErrorǁ__init____mutmut_26, 
        'xǁStateErrorǁ__init____mutmut_27': xǁStateErrorǁ__init____mutmut_27, 
        'xǁStateErrorǁ__init____mutmut_28': xǁStateErrorǁ__init____mutmut_28, 
        'xǁStateErrorǁ__init____mutmut_29': xǁStateErrorǁ__init____mutmut_29, 
        'xǁStateErrorǁ__init____mutmut_30': xǁStateErrorǁ__init____mutmut_30
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStateErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁStateErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁStateErrorǁ__init____mutmut_orig)
    xǁStateErrorǁ__init____mutmut_orig.__name__ = 'xǁStateErrorǁ__init__'

    def xǁStateErrorǁ_default_code__mutmut_orig(self) -> str:
        return "STATE_ERROR"

    def xǁStateErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXSTATE_ERRORXX"

    def xǁStateErrorǁ_default_code__mutmut_2(self) -> str:
        return "state_error"
    
    xǁStateErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStateErrorǁ_default_code__mutmut_1': xǁStateErrorǁ_default_code__mutmut_1, 
        'xǁStateErrorǁ_default_code__mutmut_2': xǁStateErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStateErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁStateErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁStateErrorǁ_default_code__mutmut_orig)
    xǁStateErrorǁ_default_code__mutmut_orig.__name__ = 'xǁStateErrorǁ_default_code'


class ConcurrencyError(FoundationError):
    """Raised when concurrency conflicts occur.

    Args:
        message: Error message describing the concurrency issue.
        conflict_type: Optional type of conflict (lock, version, etc.).
        version_expected: Optional expected version.
        version_actual: Optional actual version.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise ConcurrencyError("Optimistic lock failure")
        >>> raise ConcurrencyError("Version mismatch", version_expected=1, version_actual=2)

    """

    def xǁConcurrencyErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = None
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault(None, {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", None)["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault({})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", )["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("XXcontextXX", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("CONTEXT", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["XXconcurrency.typeXX"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["CONCURRENCY.TYPE"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = None
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_12(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault(None, {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_13(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", None)["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_14(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault({})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_15(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", )["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_16(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("XXcontextXX", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_17(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("CONTEXT", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_18(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["XXconcurrency.version_expectedXX"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_19(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["CONCURRENCY.VERSION_EXPECTED"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_20(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(None)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_21(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_22(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = None
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_23(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault(None, {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_24(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", None)["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_25(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault({})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_26(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", )["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_27(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("XXcontextXX", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_28(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("CONTEXT", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_29(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["XXconcurrency.version_actualXX"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_30(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["CONCURRENCY.VERSION_ACTUAL"] = str(version_actual)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_31(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(None)
        super().__init__(message, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_32(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(None, **kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_33(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(**kwargs)

    def xǁConcurrencyErrorǁ__init____mutmut_34(
        self,
        message: str,
        *,
        conflict_type: str | None = None,
        version_expected: Any = None,
        version_actual: Any = None,
        **kwargs: Any,
    ) -> None:
        if conflict_type:
            kwargs.setdefault("context", {})["concurrency.type"] = conflict_type
        if version_expected is not None:
            kwargs.setdefault("context", {})["concurrency.version_expected"] = str(version_expected)
        if version_actual is not None:
            kwargs.setdefault("context", {})["concurrency.version_actual"] = str(version_actual)
        super().__init__(message, )
    
    xǁConcurrencyErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConcurrencyErrorǁ__init____mutmut_1': xǁConcurrencyErrorǁ__init____mutmut_1, 
        'xǁConcurrencyErrorǁ__init____mutmut_2': xǁConcurrencyErrorǁ__init____mutmut_2, 
        'xǁConcurrencyErrorǁ__init____mutmut_3': xǁConcurrencyErrorǁ__init____mutmut_3, 
        'xǁConcurrencyErrorǁ__init____mutmut_4': xǁConcurrencyErrorǁ__init____mutmut_4, 
        'xǁConcurrencyErrorǁ__init____mutmut_5': xǁConcurrencyErrorǁ__init____mutmut_5, 
        'xǁConcurrencyErrorǁ__init____mutmut_6': xǁConcurrencyErrorǁ__init____mutmut_6, 
        'xǁConcurrencyErrorǁ__init____mutmut_7': xǁConcurrencyErrorǁ__init____mutmut_7, 
        'xǁConcurrencyErrorǁ__init____mutmut_8': xǁConcurrencyErrorǁ__init____mutmut_8, 
        'xǁConcurrencyErrorǁ__init____mutmut_9': xǁConcurrencyErrorǁ__init____mutmut_9, 
        'xǁConcurrencyErrorǁ__init____mutmut_10': xǁConcurrencyErrorǁ__init____mutmut_10, 
        'xǁConcurrencyErrorǁ__init____mutmut_11': xǁConcurrencyErrorǁ__init____mutmut_11, 
        'xǁConcurrencyErrorǁ__init____mutmut_12': xǁConcurrencyErrorǁ__init____mutmut_12, 
        'xǁConcurrencyErrorǁ__init____mutmut_13': xǁConcurrencyErrorǁ__init____mutmut_13, 
        'xǁConcurrencyErrorǁ__init____mutmut_14': xǁConcurrencyErrorǁ__init____mutmut_14, 
        'xǁConcurrencyErrorǁ__init____mutmut_15': xǁConcurrencyErrorǁ__init____mutmut_15, 
        'xǁConcurrencyErrorǁ__init____mutmut_16': xǁConcurrencyErrorǁ__init____mutmut_16, 
        'xǁConcurrencyErrorǁ__init____mutmut_17': xǁConcurrencyErrorǁ__init____mutmut_17, 
        'xǁConcurrencyErrorǁ__init____mutmut_18': xǁConcurrencyErrorǁ__init____mutmut_18, 
        'xǁConcurrencyErrorǁ__init____mutmut_19': xǁConcurrencyErrorǁ__init____mutmut_19, 
        'xǁConcurrencyErrorǁ__init____mutmut_20': xǁConcurrencyErrorǁ__init____mutmut_20, 
        'xǁConcurrencyErrorǁ__init____mutmut_21': xǁConcurrencyErrorǁ__init____mutmut_21, 
        'xǁConcurrencyErrorǁ__init____mutmut_22': xǁConcurrencyErrorǁ__init____mutmut_22, 
        'xǁConcurrencyErrorǁ__init____mutmut_23': xǁConcurrencyErrorǁ__init____mutmut_23, 
        'xǁConcurrencyErrorǁ__init____mutmut_24': xǁConcurrencyErrorǁ__init____mutmut_24, 
        'xǁConcurrencyErrorǁ__init____mutmut_25': xǁConcurrencyErrorǁ__init____mutmut_25, 
        'xǁConcurrencyErrorǁ__init____mutmut_26': xǁConcurrencyErrorǁ__init____mutmut_26, 
        'xǁConcurrencyErrorǁ__init____mutmut_27': xǁConcurrencyErrorǁ__init____mutmut_27, 
        'xǁConcurrencyErrorǁ__init____mutmut_28': xǁConcurrencyErrorǁ__init____mutmut_28, 
        'xǁConcurrencyErrorǁ__init____mutmut_29': xǁConcurrencyErrorǁ__init____mutmut_29, 
        'xǁConcurrencyErrorǁ__init____mutmut_30': xǁConcurrencyErrorǁ__init____mutmut_30, 
        'xǁConcurrencyErrorǁ__init____mutmut_31': xǁConcurrencyErrorǁ__init____mutmut_31, 
        'xǁConcurrencyErrorǁ__init____mutmut_32': xǁConcurrencyErrorǁ__init____mutmut_32, 
        'xǁConcurrencyErrorǁ__init____mutmut_33': xǁConcurrencyErrorǁ__init____mutmut_33, 
        'xǁConcurrencyErrorǁ__init____mutmut_34': xǁConcurrencyErrorǁ__init____mutmut_34
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConcurrencyErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁConcurrencyErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁConcurrencyErrorǁ__init____mutmut_orig)
    xǁConcurrencyErrorǁ__init____mutmut_orig.__name__ = 'xǁConcurrencyErrorǁ__init__'

    def xǁConcurrencyErrorǁ_default_code__mutmut_orig(self) -> str:
        return "CONCURRENCY_ERROR"

    def xǁConcurrencyErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXCONCURRENCY_ERRORXX"

    def xǁConcurrencyErrorǁ_default_code__mutmut_2(self) -> str:
        return "concurrency_error"
    
    xǁConcurrencyErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConcurrencyErrorǁ_default_code__mutmut_1': xǁConcurrencyErrorǁ_default_code__mutmut_1, 
        'xǁConcurrencyErrorǁ_default_code__mutmut_2': xǁConcurrencyErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConcurrencyErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁConcurrencyErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁConcurrencyErrorǁ_default_code__mutmut_orig)
    xǁConcurrencyErrorǁ_default_code__mutmut_orig.__name__ = 'xǁConcurrencyErrorǁ_default_code'


class RateLimitExceededError(FoundationError):
    """Raised when a rate limit is exceeded.

    Args:
        message: Error message describing the rate limit violation.
        limit: The rate limit that was exceeded (requests/messages per time unit).
        retry_after: Seconds to wait before retrying.
        current_rate: Optional current rate at time of error.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise RateLimitExceededError("Log rate limit exceeded", limit=100.0, retry_after=1.0)
        >>> raise RateLimitExceededError("API rate limit", limit=1000, retry_after=60, current_rate=1050)

    """

    def xǁRateLimitExceededErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = None
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault(None, {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", None)["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault({})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", )["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("XXcontextXX", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("CONTEXT", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["XXrate_limit.limitXX"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["RATE_LIMIT.LIMIT"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_12(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = None
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_13(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault(None, {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_14(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", None)["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_15(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault({})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_16(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", )["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_17(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("XXcontextXX", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_18(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("CONTEXT", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_19(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["XXrate_limit.retry_afterXX"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_20(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["RATE_LIMIT.RETRY_AFTER"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_21(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_22(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = None
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_23(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault(None, {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_24(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", None)["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_25(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault({})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_26(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", )["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_27(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("XXcontextXX", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_28(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("CONTEXT", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_29(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["XXrate_limit.current_rateXX"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_30(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["RATE_LIMIT.CURRENT_RATE"] = current_rate
        super().__init__(message, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_31(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(None, **kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_32(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(**kwargs)

    def xǁRateLimitExceededErrorǁ__init____mutmut_33(
        self,
        message: str,
        *,
        limit: float | None = None,
        retry_after: float | None = None,
        current_rate: float | None = None,
        **kwargs: Any,
    ) -> None:
        if limit is not None:
            kwargs.setdefault("context", {})["rate_limit.limit"] = limit
        if retry_after is not None:
            kwargs.setdefault("context", {})["rate_limit.retry_after"] = retry_after
        if current_rate is not None:
            kwargs.setdefault("context", {})["rate_limit.current_rate"] = current_rate
        super().__init__(message, )
    
    xǁRateLimitExceededErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRateLimitExceededErrorǁ__init____mutmut_1': xǁRateLimitExceededErrorǁ__init____mutmut_1, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_2': xǁRateLimitExceededErrorǁ__init____mutmut_2, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_3': xǁRateLimitExceededErrorǁ__init____mutmut_3, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_4': xǁRateLimitExceededErrorǁ__init____mutmut_4, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_5': xǁRateLimitExceededErrorǁ__init____mutmut_5, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_6': xǁRateLimitExceededErrorǁ__init____mutmut_6, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_7': xǁRateLimitExceededErrorǁ__init____mutmut_7, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_8': xǁRateLimitExceededErrorǁ__init____mutmut_8, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_9': xǁRateLimitExceededErrorǁ__init____mutmut_9, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_10': xǁRateLimitExceededErrorǁ__init____mutmut_10, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_11': xǁRateLimitExceededErrorǁ__init____mutmut_11, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_12': xǁRateLimitExceededErrorǁ__init____mutmut_12, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_13': xǁRateLimitExceededErrorǁ__init____mutmut_13, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_14': xǁRateLimitExceededErrorǁ__init____mutmut_14, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_15': xǁRateLimitExceededErrorǁ__init____mutmut_15, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_16': xǁRateLimitExceededErrorǁ__init____mutmut_16, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_17': xǁRateLimitExceededErrorǁ__init____mutmut_17, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_18': xǁRateLimitExceededErrorǁ__init____mutmut_18, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_19': xǁRateLimitExceededErrorǁ__init____mutmut_19, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_20': xǁRateLimitExceededErrorǁ__init____mutmut_20, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_21': xǁRateLimitExceededErrorǁ__init____mutmut_21, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_22': xǁRateLimitExceededErrorǁ__init____mutmut_22, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_23': xǁRateLimitExceededErrorǁ__init____mutmut_23, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_24': xǁRateLimitExceededErrorǁ__init____mutmut_24, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_25': xǁRateLimitExceededErrorǁ__init____mutmut_25, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_26': xǁRateLimitExceededErrorǁ__init____mutmut_26, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_27': xǁRateLimitExceededErrorǁ__init____mutmut_27, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_28': xǁRateLimitExceededErrorǁ__init____mutmut_28, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_29': xǁRateLimitExceededErrorǁ__init____mutmut_29, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_30': xǁRateLimitExceededErrorǁ__init____mutmut_30, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_31': xǁRateLimitExceededErrorǁ__init____mutmut_31, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_32': xǁRateLimitExceededErrorǁ__init____mutmut_32, 
        'xǁRateLimitExceededErrorǁ__init____mutmut_33': xǁRateLimitExceededErrorǁ__init____mutmut_33
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRateLimitExceededErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁRateLimitExceededErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁRateLimitExceededErrorǁ__init____mutmut_orig)
    xǁRateLimitExceededErrorǁ__init____mutmut_orig.__name__ = 'xǁRateLimitExceededErrorǁ__init__'

    def xǁRateLimitExceededErrorǁ_default_code__mutmut_orig(self) -> str:
        return "INTEGRATION_RATE_LIMIT"

    def xǁRateLimitExceededErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXINTEGRATION_RATE_LIMITXX"

    def xǁRateLimitExceededErrorǁ_default_code__mutmut_2(self) -> str:
        return "integration_rate_limit"
    
    xǁRateLimitExceededErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁRateLimitExceededErrorǁ_default_code__mutmut_1': xǁRateLimitExceededErrorǁ_default_code__mutmut_1, 
        'xǁRateLimitExceededErrorǁ_default_code__mutmut_2': xǁRateLimitExceededErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁRateLimitExceededErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁRateLimitExceededErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁRateLimitExceededErrorǁ_default_code__mutmut_orig)
    xǁRateLimitExceededErrorǁ_default_code__mutmut_orig.__name__ = 'xǁRateLimitExceededErrorǁ_default_code'


# <3 🧱🤝🐛🪄
