# provide/foundation/errors/resources.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any

from provide.foundation.errors.base import FoundationError

"""Resource and filesystem-related exceptions."""
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


class ResourceError(FoundationError):
    """Raised when resource operations fail.

    Args:
        message: Error message describing the resource issue.
        resource_type: Optional type of resource (file, network, etc.).
        resource_path: Optional path or identifier of the resource.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise ResourceError("File not found")
        >>> raise ResourceError("Permission denied", resource_type="file", resource_path="/etc/config")

    """

    def xǁResourceErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_path: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["resource.type"] = resource_type
        if resource_path:
            kwargs.setdefault("context", {})["resource.path"] = resource_path
        super().__init__(message, **kwargs)

    def xǁResourceErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_path: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["resource.type"] = None
        if resource_path:
            kwargs.setdefault("context", {})["resource.path"] = resource_path
        super().__init__(message, **kwargs)

    def xǁResourceErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_path: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault(None, {})["resource.type"] = resource_type
        if resource_path:
            kwargs.setdefault("context", {})["resource.path"] = resource_path
        super().__init__(message, **kwargs)

    def xǁResourceErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_path: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", None)["resource.type"] = resource_type
        if resource_path:
            kwargs.setdefault("context", {})["resource.path"] = resource_path
        super().__init__(message, **kwargs)

    def xǁResourceErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_path: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault({})["resource.type"] = resource_type
        if resource_path:
            kwargs.setdefault("context", {})["resource.path"] = resource_path
        super().__init__(message, **kwargs)

    def xǁResourceErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_path: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", )["resource.type"] = resource_type
        if resource_path:
            kwargs.setdefault("context", {})["resource.path"] = resource_path
        super().__init__(message, **kwargs)

    def xǁResourceErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_path: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("XXcontextXX", {})["resource.type"] = resource_type
        if resource_path:
            kwargs.setdefault("context", {})["resource.path"] = resource_path
        super().__init__(message, **kwargs)

    def xǁResourceErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_path: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("CONTEXT", {})["resource.type"] = resource_type
        if resource_path:
            kwargs.setdefault("context", {})["resource.path"] = resource_path
        super().__init__(message, **kwargs)

    def xǁResourceErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_path: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["XXresource.typeXX"] = resource_type
        if resource_path:
            kwargs.setdefault("context", {})["resource.path"] = resource_path
        super().__init__(message, **kwargs)

    def xǁResourceErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_path: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["RESOURCE.TYPE"] = resource_type
        if resource_path:
            kwargs.setdefault("context", {})["resource.path"] = resource_path
        super().__init__(message, **kwargs)

    def xǁResourceErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_path: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["resource.type"] = resource_type
        if resource_path:
            kwargs.setdefault("context", {})["resource.path"] = None
        super().__init__(message, **kwargs)

    def xǁResourceErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_path: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["resource.type"] = resource_type
        if resource_path:
            kwargs.setdefault(None, {})["resource.path"] = resource_path
        super().__init__(message, **kwargs)

    def xǁResourceErrorǁ__init____mutmut_12(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_path: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["resource.type"] = resource_type
        if resource_path:
            kwargs.setdefault("context", None)["resource.path"] = resource_path
        super().__init__(message, **kwargs)

    def xǁResourceErrorǁ__init____mutmut_13(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_path: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["resource.type"] = resource_type
        if resource_path:
            kwargs.setdefault({})["resource.path"] = resource_path
        super().__init__(message, **kwargs)

    def xǁResourceErrorǁ__init____mutmut_14(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_path: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["resource.type"] = resource_type
        if resource_path:
            kwargs.setdefault("context", )["resource.path"] = resource_path
        super().__init__(message, **kwargs)

    def xǁResourceErrorǁ__init____mutmut_15(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_path: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["resource.type"] = resource_type
        if resource_path:
            kwargs.setdefault("XXcontextXX", {})["resource.path"] = resource_path
        super().__init__(message, **kwargs)

    def xǁResourceErrorǁ__init____mutmut_16(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_path: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["resource.type"] = resource_type
        if resource_path:
            kwargs.setdefault("CONTEXT", {})["resource.path"] = resource_path
        super().__init__(message, **kwargs)

    def xǁResourceErrorǁ__init____mutmut_17(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_path: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["resource.type"] = resource_type
        if resource_path:
            kwargs.setdefault("context", {})["XXresource.pathXX"] = resource_path
        super().__init__(message, **kwargs)

    def xǁResourceErrorǁ__init____mutmut_18(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_path: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["resource.type"] = resource_type
        if resource_path:
            kwargs.setdefault("context", {})["RESOURCE.PATH"] = resource_path
        super().__init__(message, **kwargs)

    def xǁResourceErrorǁ__init____mutmut_19(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_path: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["resource.type"] = resource_type
        if resource_path:
            kwargs.setdefault("context", {})["resource.path"] = resource_path
        super().__init__(None, **kwargs)

    def xǁResourceErrorǁ__init____mutmut_20(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_path: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["resource.type"] = resource_type
        if resource_path:
            kwargs.setdefault("context", {})["resource.path"] = resource_path
        super().__init__(**kwargs)

    def xǁResourceErrorǁ__init____mutmut_21(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_path: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["resource.type"] = resource_type
        if resource_path:
            kwargs.setdefault("context", {})["resource.path"] = resource_path
        super().__init__(message, )
    
    xǁResourceErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁResourceErrorǁ__init____mutmut_1': xǁResourceErrorǁ__init____mutmut_1, 
        'xǁResourceErrorǁ__init____mutmut_2': xǁResourceErrorǁ__init____mutmut_2, 
        'xǁResourceErrorǁ__init____mutmut_3': xǁResourceErrorǁ__init____mutmut_3, 
        'xǁResourceErrorǁ__init____mutmut_4': xǁResourceErrorǁ__init____mutmut_4, 
        'xǁResourceErrorǁ__init____mutmut_5': xǁResourceErrorǁ__init____mutmut_5, 
        'xǁResourceErrorǁ__init____mutmut_6': xǁResourceErrorǁ__init____mutmut_6, 
        'xǁResourceErrorǁ__init____mutmut_7': xǁResourceErrorǁ__init____mutmut_7, 
        'xǁResourceErrorǁ__init____mutmut_8': xǁResourceErrorǁ__init____mutmut_8, 
        'xǁResourceErrorǁ__init____mutmut_9': xǁResourceErrorǁ__init____mutmut_9, 
        'xǁResourceErrorǁ__init____mutmut_10': xǁResourceErrorǁ__init____mutmut_10, 
        'xǁResourceErrorǁ__init____mutmut_11': xǁResourceErrorǁ__init____mutmut_11, 
        'xǁResourceErrorǁ__init____mutmut_12': xǁResourceErrorǁ__init____mutmut_12, 
        'xǁResourceErrorǁ__init____mutmut_13': xǁResourceErrorǁ__init____mutmut_13, 
        'xǁResourceErrorǁ__init____mutmut_14': xǁResourceErrorǁ__init____mutmut_14, 
        'xǁResourceErrorǁ__init____mutmut_15': xǁResourceErrorǁ__init____mutmut_15, 
        'xǁResourceErrorǁ__init____mutmut_16': xǁResourceErrorǁ__init____mutmut_16, 
        'xǁResourceErrorǁ__init____mutmut_17': xǁResourceErrorǁ__init____mutmut_17, 
        'xǁResourceErrorǁ__init____mutmut_18': xǁResourceErrorǁ__init____mutmut_18, 
        'xǁResourceErrorǁ__init____mutmut_19': xǁResourceErrorǁ__init____mutmut_19, 
        'xǁResourceErrorǁ__init____mutmut_20': xǁResourceErrorǁ__init____mutmut_20, 
        'xǁResourceErrorǁ__init____mutmut_21': xǁResourceErrorǁ__init____mutmut_21
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁResourceErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁResourceErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁResourceErrorǁ__init____mutmut_orig)
    xǁResourceErrorǁ__init____mutmut_orig.__name__ = 'xǁResourceErrorǁ__init__'

    def xǁResourceErrorǁ_default_code__mutmut_orig(self) -> str:
        return "RESOURCE_ERROR"

    def xǁResourceErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXRESOURCE_ERRORXX"

    def xǁResourceErrorǁ_default_code__mutmut_2(self) -> str:
        return "resource_error"
    
    xǁResourceErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁResourceErrorǁ_default_code__mutmut_1': xǁResourceErrorǁ_default_code__mutmut_1, 
        'xǁResourceErrorǁ_default_code__mutmut_2': xǁResourceErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁResourceErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁResourceErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁResourceErrorǁ_default_code__mutmut_orig)
    xǁResourceErrorǁ_default_code__mutmut_orig.__name__ = 'xǁResourceErrorǁ_default_code'


class NotFoundError(FoundationError):
    """Raised when a requested resource cannot be found.

    Args:
        message: Error message describing what was not found.
        resource_type: Optional type of resource.
        resource_id: Optional resource identifier.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise NotFoundError("User not found")
        >>> raise NotFoundError("Entity missing", resource_type="user", resource_id="123")

    """

    def xǁNotFoundErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["notfound.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["notfound.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁNotFoundErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["notfound.type"] = None
        if resource_id:
            kwargs.setdefault("context", {})["notfound.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁNotFoundErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault(None, {})["notfound.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["notfound.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁNotFoundErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", None)["notfound.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["notfound.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁNotFoundErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault({})["notfound.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["notfound.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁNotFoundErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", )["notfound.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["notfound.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁNotFoundErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("XXcontextXX", {})["notfound.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["notfound.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁNotFoundErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("CONTEXT", {})["notfound.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["notfound.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁNotFoundErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["XXnotfound.typeXX"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["notfound.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁNotFoundErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["NOTFOUND.TYPE"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["notfound.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁNotFoundErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["notfound.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["notfound.id"] = None
        super().__init__(message, **kwargs)

    def xǁNotFoundErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["notfound.type"] = resource_type
        if resource_id:
            kwargs.setdefault(None, {})["notfound.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁNotFoundErrorǁ__init____mutmut_12(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["notfound.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", None)["notfound.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁNotFoundErrorǁ__init____mutmut_13(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["notfound.type"] = resource_type
        if resource_id:
            kwargs.setdefault({})["notfound.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁNotFoundErrorǁ__init____mutmut_14(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["notfound.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", )["notfound.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁNotFoundErrorǁ__init____mutmut_15(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["notfound.type"] = resource_type
        if resource_id:
            kwargs.setdefault("XXcontextXX", {})["notfound.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁNotFoundErrorǁ__init____mutmut_16(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["notfound.type"] = resource_type
        if resource_id:
            kwargs.setdefault("CONTEXT", {})["notfound.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁNotFoundErrorǁ__init____mutmut_17(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["notfound.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["XXnotfound.idXX"] = resource_id
        super().__init__(message, **kwargs)

    def xǁNotFoundErrorǁ__init____mutmut_18(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["notfound.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["NOTFOUND.ID"] = resource_id
        super().__init__(message, **kwargs)

    def xǁNotFoundErrorǁ__init____mutmut_19(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["notfound.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["notfound.id"] = resource_id
        super().__init__(None, **kwargs)

    def xǁNotFoundErrorǁ__init____mutmut_20(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["notfound.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["notfound.id"] = resource_id
        super().__init__(**kwargs)

    def xǁNotFoundErrorǁ__init____mutmut_21(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["notfound.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["notfound.id"] = resource_id
        super().__init__(message, )
    
    xǁNotFoundErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁNotFoundErrorǁ__init____mutmut_1': xǁNotFoundErrorǁ__init____mutmut_1, 
        'xǁNotFoundErrorǁ__init____mutmut_2': xǁNotFoundErrorǁ__init____mutmut_2, 
        'xǁNotFoundErrorǁ__init____mutmut_3': xǁNotFoundErrorǁ__init____mutmut_3, 
        'xǁNotFoundErrorǁ__init____mutmut_4': xǁNotFoundErrorǁ__init____mutmut_4, 
        'xǁNotFoundErrorǁ__init____mutmut_5': xǁNotFoundErrorǁ__init____mutmut_5, 
        'xǁNotFoundErrorǁ__init____mutmut_6': xǁNotFoundErrorǁ__init____mutmut_6, 
        'xǁNotFoundErrorǁ__init____mutmut_7': xǁNotFoundErrorǁ__init____mutmut_7, 
        'xǁNotFoundErrorǁ__init____mutmut_8': xǁNotFoundErrorǁ__init____mutmut_8, 
        'xǁNotFoundErrorǁ__init____mutmut_9': xǁNotFoundErrorǁ__init____mutmut_9, 
        'xǁNotFoundErrorǁ__init____mutmut_10': xǁNotFoundErrorǁ__init____mutmut_10, 
        'xǁNotFoundErrorǁ__init____mutmut_11': xǁNotFoundErrorǁ__init____mutmut_11, 
        'xǁNotFoundErrorǁ__init____mutmut_12': xǁNotFoundErrorǁ__init____mutmut_12, 
        'xǁNotFoundErrorǁ__init____mutmut_13': xǁNotFoundErrorǁ__init____mutmut_13, 
        'xǁNotFoundErrorǁ__init____mutmut_14': xǁNotFoundErrorǁ__init____mutmut_14, 
        'xǁNotFoundErrorǁ__init____mutmut_15': xǁNotFoundErrorǁ__init____mutmut_15, 
        'xǁNotFoundErrorǁ__init____mutmut_16': xǁNotFoundErrorǁ__init____mutmut_16, 
        'xǁNotFoundErrorǁ__init____mutmut_17': xǁNotFoundErrorǁ__init____mutmut_17, 
        'xǁNotFoundErrorǁ__init____mutmut_18': xǁNotFoundErrorǁ__init____mutmut_18, 
        'xǁNotFoundErrorǁ__init____mutmut_19': xǁNotFoundErrorǁ__init____mutmut_19, 
        'xǁNotFoundErrorǁ__init____mutmut_20': xǁNotFoundErrorǁ__init____mutmut_20, 
        'xǁNotFoundErrorǁ__init____mutmut_21': xǁNotFoundErrorǁ__init____mutmut_21
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁNotFoundErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁNotFoundErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁNotFoundErrorǁ__init____mutmut_orig)
    xǁNotFoundErrorǁ__init____mutmut_orig.__name__ = 'xǁNotFoundErrorǁ__init__'

    def xǁNotFoundErrorǁ_default_code__mutmut_orig(self) -> str:
        return "NOT_FOUND_ERROR"

    def xǁNotFoundErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXNOT_FOUND_ERRORXX"

    def xǁNotFoundErrorǁ_default_code__mutmut_2(self) -> str:
        return "not_found_error"
    
    xǁNotFoundErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁNotFoundErrorǁ_default_code__mutmut_1': xǁNotFoundErrorǁ_default_code__mutmut_1, 
        'xǁNotFoundErrorǁ_default_code__mutmut_2': xǁNotFoundErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁNotFoundErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁNotFoundErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁNotFoundErrorǁ_default_code__mutmut_orig)
    xǁNotFoundErrorǁ_default_code__mutmut_orig.__name__ = 'xǁNotFoundErrorǁ_default_code'


class AlreadyExistsError(FoundationError):
    """Raised when attempting to create a resource that already exists.

    Args:
        message: Error message describing the conflict.
        resource_type: Optional type of resource.
        resource_id: Optional resource identifier.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise AlreadyExistsError("User already registered")
        >>> raise AlreadyExistsError("Duplicate key", resource_type="user", resource_id="john@example.com")

    """

    def xǁAlreadyExistsErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["exists.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["exists.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁAlreadyExistsErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["exists.type"] = None
        if resource_id:
            kwargs.setdefault("context", {})["exists.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁAlreadyExistsErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault(None, {})["exists.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["exists.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁAlreadyExistsErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", None)["exists.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["exists.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁAlreadyExistsErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault({})["exists.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["exists.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁAlreadyExistsErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", )["exists.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["exists.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁAlreadyExistsErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("XXcontextXX", {})["exists.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["exists.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁAlreadyExistsErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("CONTEXT", {})["exists.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["exists.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁAlreadyExistsErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["XXexists.typeXX"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["exists.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁAlreadyExistsErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["EXISTS.TYPE"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["exists.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁAlreadyExistsErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["exists.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["exists.id"] = None
        super().__init__(message, **kwargs)

    def xǁAlreadyExistsErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["exists.type"] = resource_type
        if resource_id:
            kwargs.setdefault(None, {})["exists.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁAlreadyExistsErrorǁ__init____mutmut_12(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["exists.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", None)["exists.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁAlreadyExistsErrorǁ__init____mutmut_13(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["exists.type"] = resource_type
        if resource_id:
            kwargs.setdefault({})["exists.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁAlreadyExistsErrorǁ__init____mutmut_14(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["exists.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", )["exists.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁAlreadyExistsErrorǁ__init____mutmut_15(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["exists.type"] = resource_type
        if resource_id:
            kwargs.setdefault("XXcontextXX", {})["exists.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁAlreadyExistsErrorǁ__init____mutmut_16(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["exists.type"] = resource_type
        if resource_id:
            kwargs.setdefault("CONTEXT", {})["exists.id"] = resource_id
        super().__init__(message, **kwargs)

    def xǁAlreadyExistsErrorǁ__init____mutmut_17(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["exists.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["XXexists.idXX"] = resource_id
        super().__init__(message, **kwargs)

    def xǁAlreadyExistsErrorǁ__init____mutmut_18(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["exists.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["EXISTS.ID"] = resource_id
        super().__init__(message, **kwargs)

    def xǁAlreadyExistsErrorǁ__init____mutmut_19(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["exists.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["exists.id"] = resource_id
        super().__init__(None, **kwargs)

    def xǁAlreadyExistsErrorǁ__init____mutmut_20(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["exists.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["exists.id"] = resource_id
        super().__init__(**kwargs)

    def xǁAlreadyExistsErrorǁ__init____mutmut_21(
        self,
        message: str,
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        **kwargs: Any,
    ) -> None:
        if resource_type:
            kwargs.setdefault("context", {})["exists.type"] = resource_type
        if resource_id:
            kwargs.setdefault("context", {})["exists.id"] = resource_id
        super().__init__(message, )
    
    xǁAlreadyExistsErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAlreadyExistsErrorǁ__init____mutmut_1': xǁAlreadyExistsErrorǁ__init____mutmut_1, 
        'xǁAlreadyExistsErrorǁ__init____mutmut_2': xǁAlreadyExistsErrorǁ__init____mutmut_2, 
        'xǁAlreadyExistsErrorǁ__init____mutmut_3': xǁAlreadyExistsErrorǁ__init____mutmut_3, 
        'xǁAlreadyExistsErrorǁ__init____mutmut_4': xǁAlreadyExistsErrorǁ__init____mutmut_4, 
        'xǁAlreadyExistsErrorǁ__init____mutmut_5': xǁAlreadyExistsErrorǁ__init____mutmut_5, 
        'xǁAlreadyExistsErrorǁ__init____mutmut_6': xǁAlreadyExistsErrorǁ__init____mutmut_6, 
        'xǁAlreadyExistsErrorǁ__init____mutmut_7': xǁAlreadyExistsErrorǁ__init____mutmut_7, 
        'xǁAlreadyExistsErrorǁ__init____mutmut_8': xǁAlreadyExistsErrorǁ__init____mutmut_8, 
        'xǁAlreadyExistsErrorǁ__init____mutmut_9': xǁAlreadyExistsErrorǁ__init____mutmut_9, 
        'xǁAlreadyExistsErrorǁ__init____mutmut_10': xǁAlreadyExistsErrorǁ__init____mutmut_10, 
        'xǁAlreadyExistsErrorǁ__init____mutmut_11': xǁAlreadyExistsErrorǁ__init____mutmut_11, 
        'xǁAlreadyExistsErrorǁ__init____mutmut_12': xǁAlreadyExistsErrorǁ__init____mutmut_12, 
        'xǁAlreadyExistsErrorǁ__init____mutmut_13': xǁAlreadyExistsErrorǁ__init____mutmut_13, 
        'xǁAlreadyExistsErrorǁ__init____mutmut_14': xǁAlreadyExistsErrorǁ__init____mutmut_14, 
        'xǁAlreadyExistsErrorǁ__init____mutmut_15': xǁAlreadyExistsErrorǁ__init____mutmut_15, 
        'xǁAlreadyExistsErrorǁ__init____mutmut_16': xǁAlreadyExistsErrorǁ__init____mutmut_16, 
        'xǁAlreadyExistsErrorǁ__init____mutmut_17': xǁAlreadyExistsErrorǁ__init____mutmut_17, 
        'xǁAlreadyExistsErrorǁ__init____mutmut_18': xǁAlreadyExistsErrorǁ__init____mutmut_18, 
        'xǁAlreadyExistsErrorǁ__init____mutmut_19': xǁAlreadyExistsErrorǁ__init____mutmut_19, 
        'xǁAlreadyExistsErrorǁ__init____mutmut_20': xǁAlreadyExistsErrorǁ__init____mutmut_20, 
        'xǁAlreadyExistsErrorǁ__init____mutmut_21': xǁAlreadyExistsErrorǁ__init____mutmut_21
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAlreadyExistsErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁAlreadyExistsErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁAlreadyExistsErrorǁ__init____mutmut_orig)
    xǁAlreadyExistsErrorǁ__init____mutmut_orig.__name__ = 'xǁAlreadyExistsErrorǁ__init__'

    def xǁAlreadyExistsErrorǁ_default_code__mutmut_orig(self) -> str:
        return "ALREADY_EXISTS_ERROR"

    def xǁAlreadyExistsErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXALREADY_EXISTS_ERRORXX"

    def xǁAlreadyExistsErrorǁ_default_code__mutmut_2(self) -> str:
        return "already_exists_error"
    
    xǁAlreadyExistsErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁAlreadyExistsErrorǁ_default_code__mutmut_1': xǁAlreadyExistsErrorǁ_default_code__mutmut_1, 
        'xǁAlreadyExistsErrorǁ_default_code__mutmut_2': xǁAlreadyExistsErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁAlreadyExistsErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁAlreadyExistsErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁAlreadyExistsErrorǁ_default_code__mutmut_orig)
    xǁAlreadyExistsErrorǁ_default_code__mutmut_orig.__name__ = 'xǁAlreadyExistsErrorǁ_default_code'


class LockError(FoundationError):
    """Raised when file lock operations fail.

    Args:
        message: Error message describing the lock issue.
        lock_path: Optional path to the lock file.
        timeout: Optional timeout that was exceeded.
        **kwargs: Additional context passed to FoundationError.

    Examples:
        >>> raise LockError("Failed to acquire lock")
        >>> raise LockError("Lock timeout", lock_path="/tmp/app.lock", timeout=30)

    """

    def xǁLockErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        lock_path: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> None:
        if lock_path:
            kwargs.setdefault("context", {})["lock.path"] = lock_path
        if timeout is not None:
            kwargs.setdefault("context", {})["lock.timeout"] = timeout
        super().__init__(message, **kwargs)

    def xǁLockErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        lock_path: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> None:
        if lock_path:
            kwargs.setdefault("context", {})["lock.path"] = None
        if timeout is not None:
            kwargs.setdefault("context", {})["lock.timeout"] = timeout
        super().__init__(message, **kwargs)

    def xǁLockErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        lock_path: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> None:
        if lock_path:
            kwargs.setdefault(None, {})["lock.path"] = lock_path
        if timeout is not None:
            kwargs.setdefault("context", {})["lock.timeout"] = timeout
        super().__init__(message, **kwargs)

    def xǁLockErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        lock_path: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> None:
        if lock_path:
            kwargs.setdefault("context", None)["lock.path"] = lock_path
        if timeout is not None:
            kwargs.setdefault("context", {})["lock.timeout"] = timeout
        super().__init__(message, **kwargs)

    def xǁLockErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        lock_path: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> None:
        if lock_path:
            kwargs.setdefault({})["lock.path"] = lock_path
        if timeout is not None:
            kwargs.setdefault("context", {})["lock.timeout"] = timeout
        super().__init__(message, **kwargs)

    def xǁLockErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        lock_path: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> None:
        if lock_path:
            kwargs.setdefault("context", )["lock.path"] = lock_path
        if timeout is not None:
            kwargs.setdefault("context", {})["lock.timeout"] = timeout
        super().__init__(message, **kwargs)

    def xǁLockErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        lock_path: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> None:
        if lock_path:
            kwargs.setdefault("XXcontextXX", {})["lock.path"] = lock_path
        if timeout is not None:
            kwargs.setdefault("context", {})["lock.timeout"] = timeout
        super().__init__(message, **kwargs)

    def xǁLockErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        lock_path: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> None:
        if lock_path:
            kwargs.setdefault("CONTEXT", {})["lock.path"] = lock_path
        if timeout is not None:
            kwargs.setdefault("context", {})["lock.timeout"] = timeout
        super().__init__(message, **kwargs)

    def xǁLockErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        lock_path: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> None:
        if lock_path:
            kwargs.setdefault("context", {})["XXlock.pathXX"] = lock_path
        if timeout is not None:
            kwargs.setdefault("context", {})["lock.timeout"] = timeout
        super().__init__(message, **kwargs)

    def xǁLockErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        lock_path: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> None:
        if lock_path:
            kwargs.setdefault("context", {})["LOCK.PATH"] = lock_path
        if timeout is not None:
            kwargs.setdefault("context", {})["lock.timeout"] = timeout
        super().__init__(message, **kwargs)

    def xǁLockErrorǁ__init____mutmut_10(
        self,
        message: str,
        *,
        lock_path: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> None:
        if lock_path:
            kwargs.setdefault("context", {})["lock.path"] = lock_path
        if timeout is None:
            kwargs.setdefault("context", {})["lock.timeout"] = timeout
        super().__init__(message, **kwargs)

    def xǁLockErrorǁ__init____mutmut_11(
        self,
        message: str,
        *,
        lock_path: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> None:
        if lock_path:
            kwargs.setdefault("context", {})["lock.path"] = lock_path
        if timeout is not None:
            kwargs.setdefault("context", {})["lock.timeout"] = None
        super().__init__(message, **kwargs)

    def xǁLockErrorǁ__init____mutmut_12(
        self,
        message: str,
        *,
        lock_path: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> None:
        if lock_path:
            kwargs.setdefault("context", {})["lock.path"] = lock_path
        if timeout is not None:
            kwargs.setdefault(None, {})["lock.timeout"] = timeout
        super().__init__(message, **kwargs)

    def xǁLockErrorǁ__init____mutmut_13(
        self,
        message: str,
        *,
        lock_path: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> None:
        if lock_path:
            kwargs.setdefault("context", {})["lock.path"] = lock_path
        if timeout is not None:
            kwargs.setdefault("context", None)["lock.timeout"] = timeout
        super().__init__(message, **kwargs)

    def xǁLockErrorǁ__init____mutmut_14(
        self,
        message: str,
        *,
        lock_path: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> None:
        if lock_path:
            kwargs.setdefault("context", {})["lock.path"] = lock_path
        if timeout is not None:
            kwargs.setdefault({})["lock.timeout"] = timeout
        super().__init__(message, **kwargs)

    def xǁLockErrorǁ__init____mutmut_15(
        self,
        message: str,
        *,
        lock_path: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> None:
        if lock_path:
            kwargs.setdefault("context", {})["lock.path"] = lock_path
        if timeout is not None:
            kwargs.setdefault("context", )["lock.timeout"] = timeout
        super().__init__(message, **kwargs)

    def xǁLockErrorǁ__init____mutmut_16(
        self,
        message: str,
        *,
        lock_path: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> None:
        if lock_path:
            kwargs.setdefault("context", {})["lock.path"] = lock_path
        if timeout is not None:
            kwargs.setdefault("XXcontextXX", {})["lock.timeout"] = timeout
        super().__init__(message, **kwargs)

    def xǁLockErrorǁ__init____mutmut_17(
        self,
        message: str,
        *,
        lock_path: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> None:
        if lock_path:
            kwargs.setdefault("context", {})["lock.path"] = lock_path
        if timeout is not None:
            kwargs.setdefault("CONTEXT", {})["lock.timeout"] = timeout
        super().__init__(message, **kwargs)

    def xǁLockErrorǁ__init____mutmut_18(
        self,
        message: str,
        *,
        lock_path: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> None:
        if lock_path:
            kwargs.setdefault("context", {})["lock.path"] = lock_path
        if timeout is not None:
            kwargs.setdefault("context", {})["XXlock.timeoutXX"] = timeout
        super().__init__(message, **kwargs)

    def xǁLockErrorǁ__init____mutmut_19(
        self,
        message: str,
        *,
        lock_path: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> None:
        if lock_path:
            kwargs.setdefault("context", {})["lock.path"] = lock_path
        if timeout is not None:
            kwargs.setdefault("context", {})["LOCK.TIMEOUT"] = timeout
        super().__init__(message, **kwargs)

    def xǁLockErrorǁ__init____mutmut_20(
        self,
        message: str,
        *,
        lock_path: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> None:
        if lock_path:
            kwargs.setdefault("context", {})["lock.path"] = lock_path
        if timeout is not None:
            kwargs.setdefault("context", {})["lock.timeout"] = timeout
        super().__init__(None, **kwargs)

    def xǁLockErrorǁ__init____mutmut_21(
        self,
        message: str,
        *,
        lock_path: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> None:
        if lock_path:
            kwargs.setdefault("context", {})["lock.path"] = lock_path
        if timeout is not None:
            kwargs.setdefault("context", {})["lock.timeout"] = timeout
        super().__init__(**kwargs)

    def xǁLockErrorǁ__init____mutmut_22(
        self,
        message: str,
        *,
        lock_path: str | None = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> None:
        if lock_path:
            kwargs.setdefault("context", {})["lock.path"] = lock_path
        if timeout is not None:
            kwargs.setdefault("context", {})["lock.timeout"] = timeout
        super().__init__(message, )
    
    xǁLockErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLockErrorǁ__init____mutmut_1': xǁLockErrorǁ__init____mutmut_1, 
        'xǁLockErrorǁ__init____mutmut_2': xǁLockErrorǁ__init____mutmut_2, 
        'xǁLockErrorǁ__init____mutmut_3': xǁLockErrorǁ__init____mutmut_3, 
        'xǁLockErrorǁ__init____mutmut_4': xǁLockErrorǁ__init____mutmut_4, 
        'xǁLockErrorǁ__init____mutmut_5': xǁLockErrorǁ__init____mutmut_5, 
        'xǁLockErrorǁ__init____mutmut_6': xǁLockErrorǁ__init____mutmut_6, 
        'xǁLockErrorǁ__init____mutmut_7': xǁLockErrorǁ__init____mutmut_7, 
        'xǁLockErrorǁ__init____mutmut_8': xǁLockErrorǁ__init____mutmut_8, 
        'xǁLockErrorǁ__init____mutmut_9': xǁLockErrorǁ__init____mutmut_9, 
        'xǁLockErrorǁ__init____mutmut_10': xǁLockErrorǁ__init____mutmut_10, 
        'xǁLockErrorǁ__init____mutmut_11': xǁLockErrorǁ__init____mutmut_11, 
        'xǁLockErrorǁ__init____mutmut_12': xǁLockErrorǁ__init____mutmut_12, 
        'xǁLockErrorǁ__init____mutmut_13': xǁLockErrorǁ__init____mutmut_13, 
        'xǁLockErrorǁ__init____mutmut_14': xǁLockErrorǁ__init____mutmut_14, 
        'xǁLockErrorǁ__init____mutmut_15': xǁLockErrorǁ__init____mutmut_15, 
        'xǁLockErrorǁ__init____mutmut_16': xǁLockErrorǁ__init____mutmut_16, 
        'xǁLockErrorǁ__init____mutmut_17': xǁLockErrorǁ__init____mutmut_17, 
        'xǁLockErrorǁ__init____mutmut_18': xǁLockErrorǁ__init____mutmut_18, 
        'xǁLockErrorǁ__init____mutmut_19': xǁLockErrorǁ__init____mutmut_19, 
        'xǁLockErrorǁ__init____mutmut_20': xǁLockErrorǁ__init____mutmut_20, 
        'xǁLockErrorǁ__init____mutmut_21': xǁLockErrorǁ__init____mutmut_21, 
        'xǁLockErrorǁ__init____mutmut_22': xǁLockErrorǁ__init____mutmut_22
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLockErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁLockErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁLockErrorǁ__init____mutmut_orig)
    xǁLockErrorǁ__init____mutmut_orig.__name__ = 'xǁLockErrorǁ__init__'

    def xǁLockErrorǁ_default_code__mutmut_orig(self) -> str:
        return "LOCK_ERROR"

    def xǁLockErrorǁ_default_code__mutmut_1(self) -> str:
        return "XXLOCK_ERRORXX"

    def xǁLockErrorǁ_default_code__mutmut_2(self) -> str:
        return "lock_error"
    
    xǁLockErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁLockErrorǁ_default_code__mutmut_1': xǁLockErrorǁ_default_code__mutmut_1, 
        'xǁLockErrorǁ_default_code__mutmut_2': xǁLockErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁLockErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁLockErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁLockErrorǁ_default_code__mutmut_orig)
    xǁLockErrorǁ_default_code__mutmut_orig.__name__ = 'xǁLockErrorǁ_default_code'


# <3 🧱🤝🐛🪄
