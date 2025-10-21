# provide/foundation/errors/base.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any

"""Base exception class for Foundation."""
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


class FoundationError(Exception):
    """Base exception for all Foundation errors.

    Args:
        message: Human-readable error message.
        code: Optional error code for programmatic handling.
        context: Optional context dictionary with diagnostic data.
        cause: Optional underlying exception that caused this error.
        **extra_context: Additional key-value pairs added to context.

    Examples:
        >>> raise FoundationError("Operation failed")
        >>> raise FoundationError("Operation failed", code="OP_001")
        >>> raise FoundationError("Operation failed", user_id=123, retry_count=3)

    """

    def xǁFoundationErrorǁ__init____mutmut_orig(
        self,
        message: str,
        *,
        code: str | None = None,
        context: dict[str, Any] | None = None,
        cause: Exception | None = None,
        **extra_context: Any,
    ) -> None:
        self.message = message
        self.code = code or self._default_code()
        self.context = context or {}
        self.context.update(extra_context)
        self.cause = cause
        if cause:
            self.__cause__ = cause
        super().__init__(message)

    def xǁFoundationErrorǁ__init____mutmut_1(
        self,
        message: str,
        *,
        code: str | None = None,
        context: dict[str, Any] | None = None,
        cause: Exception | None = None,
        **extra_context: Any,
    ) -> None:
        self.message = None
        self.code = code or self._default_code()
        self.context = context or {}
        self.context.update(extra_context)
        self.cause = cause
        if cause:
            self.__cause__ = cause
        super().__init__(message)

    def xǁFoundationErrorǁ__init____mutmut_2(
        self,
        message: str,
        *,
        code: str | None = None,
        context: dict[str, Any] | None = None,
        cause: Exception | None = None,
        **extra_context: Any,
    ) -> None:
        self.message = message
        self.code = None
        self.context = context or {}
        self.context.update(extra_context)
        self.cause = cause
        if cause:
            self.__cause__ = cause
        super().__init__(message)

    def xǁFoundationErrorǁ__init____mutmut_3(
        self,
        message: str,
        *,
        code: str | None = None,
        context: dict[str, Any] | None = None,
        cause: Exception | None = None,
        **extra_context: Any,
    ) -> None:
        self.message = message
        self.code = code and self._default_code()
        self.context = context or {}
        self.context.update(extra_context)
        self.cause = cause
        if cause:
            self.__cause__ = cause
        super().__init__(message)

    def xǁFoundationErrorǁ__init____mutmut_4(
        self,
        message: str,
        *,
        code: str | None = None,
        context: dict[str, Any] | None = None,
        cause: Exception | None = None,
        **extra_context: Any,
    ) -> None:
        self.message = message
        self.code = code or self._default_code()
        self.context = None
        self.context.update(extra_context)
        self.cause = cause
        if cause:
            self.__cause__ = cause
        super().__init__(message)

    def xǁFoundationErrorǁ__init____mutmut_5(
        self,
        message: str,
        *,
        code: str | None = None,
        context: dict[str, Any] | None = None,
        cause: Exception | None = None,
        **extra_context: Any,
    ) -> None:
        self.message = message
        self.code = code or self._default_code()
        self.context = context and {}
        self.context.update(extra_context)
        self.cause = cause
        if cause:
            self.__cause__ = cause
        super().__init__(message)

    def xǁFoundationErrorǁ__init____mutmut_6(
        self,
        message: str,
        *,
        code: str | None = None,
        context: dict[str, Any] | None = None,
        cause: Exception | None = None,
        **extra_context: Any,
    ) -> None:
        self.message = message
        self.code = code or self._default_code()
        self.context = context or {}
        self.context.update(None)
        self.cause = cause
        if cause:
            self.__cause__ = cause
        super().__init__(message)

    def xǁFoundationErrorǁ__init____mutmut_7(
        self,
        message: str,
        *,
        code: str | None = None,
        context: dict[str, Any] | None = None,
        cause: Exception | None = None,
        **extra_context: Any,
    ) -> None:
        self.message = message
        self.code = code or self._default_code()
        self.context = context or {}
        self.context.update(extra_context)
        self.cause = None
        if cause:
            self.__cause__ = cause
        super().__init__(message)

    def xǁFoundationErrorǁ__init____mutmut_8(
        self,
        message: str,
        *,
        code: str | None = None,
        context: dict[str, Any] | None = None,
        cause: Exception | None = None,
        **extra_context: Any,
    ) -> None:
        self.message = message
        self.code = code or self._default_code()
        self.context = context or {}
        self.context.update(extra_context)
        self.cause = cause
        if cause:
            self.__cause__ = None
        super().__init__(message)

    def xǁFoundationErrorǁ__init____mutmut_9(
        self,
        message: str,
        *,
        code: str | None = None,
        context: dict[str, Any] | None = None,
        cause: Exception | None = None,
        **extra_context: Any,
    ) -> None:
        self.message = message
        self.code = code or self._default_code()
        self.context = context or {}
        self.context.update(extra_context)
        self.cause = cause
        if cause:
            self.__cause__ = cause
        super().__init__(None)
    
    xǁFoundationErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFoundationErrorǁ__init____mutmut_1': xǁFoundationErrorǁ__init____mutmut_1, 
        'xǁFoundationErrorǁ__init____mutmut_2': xǁFoundationErrorǁ__init____mutmut_2, 
        'xǁFoundationErrorǁ__init____mutmut_3': xǁFoundationErrorǁ__init____mutmut_3, 
        'xǁFoundationErrorǁ__init____mutmut_4': xǁFoundationErrorǁ__init____mutmut_4, 
        'xǁFoundationErrorǁ__init____mutmut_5': xǁFoundationErrorǁ__init____mutmut_5, 
        'xǁFoundationErrorǁ__init____mutmut_6': xǁFoundationErrorǁ__init____mutmut_6, 
        'xǁFoundationErrorǁ__init____mutmut_7': xǁFoundationErrorǁ__init____mutmut_7, 
        'xǁFoundationErrorǁ__init____mutmut_8': xǁFoundationErrorǁ__init____mutmut_8, 
        'xǁFoundationErrorǁ__init____mutmut_9': xǁFoundationErrorǁ__init____mutmut_9
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFoundationErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁFoundationErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁFoundationErrorǁ__init____mutmut_orig)
    xǁFoundationErrorǁ__init____mutmut_orig.__name__ = 'xǁFoundationErrorǁ__init__'

    def xǁFoundationErrorǁ_default_code__mutmut_orig(self) -> str:
        """Return default error code for this exception type."""
        return "PROVIDE_ERROR"

    def xǁFoundationErrorǁ_default_code__mutmut_1(self) -> str:
        """Return default error code for this exception type."""
        return "XXPROVIDE_ERRORXX"

    def xǁFoundationErrorǁ_default_code__mutmut_2(self) -> str:
        """Return default error code for this exception type."""
        return "provide_error"
    
    xǁFoundationErrorǁ_default_code__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFoundationErrorǁ_default_code__mutmut_1': xǁFoundationErrorǁ_default_code__mutmut_1, 
        'xǁFoundationErrorǁ_default_code__mutmut_2': xǁFoundationErrorǁ_default_code__mutmut_2
    }
    
    def _default_code(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFoundationErrorǁ_default_code__mutmut_orig"), object.__getattribute__(self, "xǁFoundationErrorǁ_default_code__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _default_code.__signature__ = _mutmut_signature(xǁFoundationErrorǁ_default_code__mutmut_orig)
    xǁFoundationErrorǁ_default_code__mutmut_orig.__name__ = 'xǁFoundationErrorǁ_default_code'

    def xǁFoundationErrorǁadd_context__mutmut_orig(self, key: str, value: Any) -> FoundationError:
        """Add context data to the error.

        Args:
            key: Context key (use dots for namespacing, e.g., 'aws.region').
            value: Context value.

        Returns:
            Self for method chaining.

        """
        self.context[key] = value
        return self

    def xǁFoundationErrorǁadd_context__mutmut_1(self, key: str, value: Any) -> FoundationError:
        """Add context data to the error.

        Args:
            key: Context key (use dots for namespacing, e.g., 'aws.region').
            value: Context value.

        Returns:
            Self for method chaining.

        """
        self.context[key] = None
        return self
    
    xǁFoundationErrorǁadd_context__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFoundationErrorǁadd_context__mutmut_1': xǁFoundationErrorǁadd_context__mutmut_1
    }
    
    def add_context(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFoundationErrorǁadd_context__mutmut_orig"), object.__getattribute__(self, "xǁFoundationErrorǁadd_context__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_context.__signature__ = _mutmut_signature(xǁFoundationErrorǁadd_context__mutmut_orig)
    xǁFoundationErrorǁadd_context__mutmut_orig.__name__ = 'xǁFoundationErrorǁadd_context'

    def xǁFoundationErrorǁto_dict__mutmut_orig(self) -> dict[str, Any]:
        """Convert exception to dictionary for structured logging.

        Returns:
            Dictionary representation suitable for logging/serialization.

        """
        result = {
            "error.type": self.__class__.__name__,
            "error.message": self.message,
            "error.code": self.code,
        }

        # Add context with error prefix
        for key, value in self.context.items():
            # If key already has a prefix, use it; otherwise add error prefix
            if "." in key:
                result[key] = value
            else:
                result[f"error.{key}"] = value

        if self.cause:
            result["error.cause"] = str(self.cause)
            result["error.cause_type"] = type(self.cause).__name__

        return result

    def xǁFoundationErrorǁto_dict__mutmut_1(self) -> dict[str, Any]:
        """Convert exception to dictionary for structured logging.

        Returns:
            Dictionary representation suitable for logging/serialization.

        """
        result = None

        # Add context with error prefix
        for key, value in self.context.items():
            # If key already has a prefix, use it; otherwise add error prefix
            if "." in key:
                result[key] = value
            else:
                result[f"error.{key}"] = value

        if self.cause:
            result["error.cause"] = str(self.cause)
            result["error.cause_type"] = type(self.cause).__name__

        return result

    def xǁFoundationErrorǁto_dict__mutmut_2(self) -> dict[str, Any]:
        """Convert exception to dictionary for structured logging.

        Returns:
            Dictionary representation suitable for logging/serialization.

        """
        result = {
            "XXerror.typeXX": self.__class__.__name__,
            "error.message": self.message,
            "error.code": self.code,
        }

        # Add context with error prefix
        for key, value in self.context.items():
            # If key already has a prefix, use it; otherwise add error prefix
            if "." in key:
                result[key] = value
            else:
                result[f"error.{key}"] = value

        if self.cause:
            result["error.cause"] = str(self.cause)
            result["error.cause_type"] = type(self.cause).__name__

        return result

    def xǁFoundationErrorǁto_dict__mutmut_3(self) -> dict[str, Any]:
        """Convert exception to dictionary for structured logging.

        Returns:
            Dictionary representation suitable for logging/serialization.

        """
        result = {
            "ERROR.TYPE": self.__class__.__name__,
            "error.message": self.message,
            "error.code": self.code,
        }

        # Add context with error prefix
        for key, value in self.context.items():
            # If key already has a prefix, use it; otherwise add error prefix
            if "." in key:
                result[key] = value
            else:
                result[f"error.{key}"] = value

        if self.cause:
            result["error.cause"] = str(self.cause)
            result["error.cause_type"] = type(self.cause).__name__

        return result

    def xǁFoundationErrorǁto_dict__mutmut_4(self) -> dict[str, Any]:
        """Convert exception to dictionary for structured logging.

        Returns:
            Dictionary representation suitable for logging/serialization.

        """
        result = {
            "error.type": self.__class__.__name__,
            "XXerror.messageXX": self.message,
            "error.code": self.code,
        }

        # Add context with error prefix
        for key, value in self.context.items():
            # If key already has a prefix, use it; otherwise add error prefix
            if "." in key:
                result[key] = value
            else:
                result[f"error.{key}"] = value

        if self.cause:
            result["error.cause"] = str(self.cause)
            result["error.cause_type"] = type(self.cause).__name__

        return result

    def xǁFoundationErrorǁto_dict__mutmut_5(self) -> dict[str, Any]:
        """Convert exception to dictionary for structured logging.

        Returns:
            Dictionary representation suitable for logging/serialization.

        """
        result = {
            "error.type": self.__class__.__name__,
            "ERROR.MESSAGE": self.message,
            "error.code": self.code,
        }

        # Add context with error prefix
        for key, value in self.context.items():
            # If key already has a prefix, use it; otherwise add error prefix
            if "." in key:
                result[key] = value
            else:
                result[f"error.{key}"] = value

        if self.cause:
            result["error.cause"] = str(self.cause)
            result["error.cause_type"] = type(self.cause).__name__

        return result

    def xǁFoundationErrorǁto_dict__mutmut_6(self) -> dict[str, Any]:
        """Convert exception to dictionary for structured logging.

        Returns:
            Dictionary representation suitable for logging/serialization.

        """
        result = {
            "error.type": self.__class__.__name__,
            "error.message": self.message,
            "XXerror.codeXX": self.code,
        }

        # Add context with error prefix
        for key, value in self.context.items():
            # If key already has a prefix, use it; otherwise add error prefix
            if "." in key:
                result[key] = value
            else:
                result[f"error.{key}"] = value

        if self.cause:
            result["error.cause"] = str(self.cause)
            result["error.cause_type"] = type(self.cause).__name__

        return result

    def xǁFoundationErrorǁto_dict__mutmut_7(self) -> dict[str, Any]:
        """Convert exception to dictionary for structured logging.

        Returns:
            Dictionary representation suitable for logging/serialization.

        """
        result = {
            "error.type": self.__class__.__name__,
            "error.message": self.message,
            "ERROR.CODE": self.code,
        }

        # Add context with error prefix
        for key, value in self.context.items():
            # If key already has a prefix, use it; otherwise add error prefix
            if "." in key:
                result[key] = value
            else:
                result[f"error.{key}"] = value

        if self.cause:
            result["error.cause"] = str(self.cause)
            result["error.cause_type"] = type(self.cause).__name__

        return result

    def xǁFoundationErrorǁto_dict__mutmut_8(self) -> dict[str, Any]:
        """Convert exception to dictionary for structured logging.

        Returns:
            Dictionary representation suitable for logging/serialization.

        """
        result = {
            "error.type": self.__class__.__name__,
            "error.message": self.message,
            "error.code": self.code,
        }

        # Add context with error prefix
        for key, value in self.context.items():
            # If key already has a prefix, use it; otherwise add error prefix
            if "XX.XX" in key:
                result[key] = value
            else:
                result[f"error.{key}"] = value

        if self.cause:
            result["error.cause"] = str(self.cause)
            result["error.cause_type"] = type(self.cause).__name__

        return result

    def xǁFoundationErrorǁto_dict__mutmut_9(self) -> dict[str, Any]:
        """Convert exception to dictionary for structured logging.

        Returns:
            Dictionary representation suitable for logging/serialization.

        """
        result = {
            "error.type": self.__class__.__name__,
            "error.message": self.message,
            "error.code": self.code,
        }

        # Add context with error prefix
        for key, value in self.context.items():
            # If key already has a prefix, use it; otherwise add error prefix
            if "." not in key:
                result[key] = value
            else:
                result[f"error.{key}"] = value

        if self.cause:
            result["error.cause"] = str(self.cause)
            result["error.cause_type"] = type(self.cause).__name__

        return result

    def xǁFoundationErrorǁto_dict__mutmut_10(self) -> dict[str, Any]:
        """Convert exception to dictionary for structured logging.

        Returns:
            Dictionary representation suitable for logging/serialization.

        """
        result = {
            "error.type": self.__class__.__name__,
            "error.message": self.message,
            "error.code": self.code,
        }

        # Add context with error prefix
        for key, value in self.context.items():
            # If key already has a prefix, use it; otherwise add error prefix
            if "." in key:
                result[key] = None
            else:
                result[f"error.{key}"] = value

        if self.cause:
            result["error.cause"] = str(self.cause)
            result["error.cause_type"] = type(self.cause).__name__

        return result

    def xǁFoundationErrorǁto_dict__mutmut_11(self) -> dict[str, Any]:
        """Convert exception to dictionary for structured logging.

        Returns:
            Dictionary representation suitable for logging/serialization.

        """
        result = {
            "error.type": self.__class__.__name__,
            "error.message": self.message,
            "error.code": self.code,
        }

        # Add context with error prefix
        for key, value in self.context.items():
            # If key already has a prefix, use it; otherwise add error prefix
            if "." in key:
                result[key] = value
            else:
                result[f"error.{key}"] = None

        if self.cause:
            result["error.cause"] = str(self.cause)
            result["error.cause_type"] = type(self.cause).__name__

        return result

    def xǁFoundationErrorǁto_dict__mutmut_12(self) -> dict[str, Any]:
        """Convert exception to dictionary for structured logging.

        Returns:
            Dictionary representation suitable for logging/serialization.

        """
        result = {
            "error.type": self.__class__.__name__,
            "error.message": self.message,
            "error.code": self.code,
        }

        # Add context with error prefix
        for key, value in self.context.items():
            # If key already has a prefix, use it; otherwise add error prefix
            if "." in key:
                result[key] = value
            else:
                result[f"error.{key}"] = value

        if self.cause:
            result["error.cause"] = None
            result["error.cause_type"] = type(self.cause).__name__

        return result

    def xǁFoundationErrorǁto_dict__mutmut_13(self) -> dict[str, Any]:
        """Convert exception to dictionary for structured logging.

        Returns:
            Dictionary representation suitable for logging/serialization.

        """
        result = {
            "error.type": self.__class__.__name__,
            "error.message": self.message,
            "error.code": self.code,
        }

        # Add context with error prefix
        for key, value in self.context.items():
            # If key already has a prefix, use it; otherwise add error prefix
            if "." in key:
                result[key] = value
            else:
                result[f"error.{key}"] = value

        if self.cause:
            result["XXerror.causeXX"] = str(self.cause)
            result["error.cause_type"] = type(self.cause).__name__

        return result

    def xǁFoundationErrorǁto_dict__mutmut_14(self) -> dict[str, Any]:
        """Convert exception to dictionary for structured logging.

        Returns:
            Dictionary representation suitable for logging/serialization.

        """
        result = {
            "error.type": self.__class__.__name__,
            "error.message": self.message,
            "error.code": self.code,
        }

        # Add context with error prefix
        for key, value in self.context.items():
            # If key already has a prefix, use it; otherwise add error prefix
            if "." in key:
                result[key] = value
            else:
                result[f"error.{key}"] = value

        if self.cause:
            result["ERROR.CAUSE"] = str(self.cause)
            result["error.cause_type"] = type(self.cause).__name__

        return result

    def xǁFoundationErrorǁto_dict__mutmut_15(self) -> dict[str, Any]:
        """Convert exception to dictionary for structured logging.

        Returns:
            Dictionary representation suitable for logging/serialization.

        """
        result = {
            "error.type": self.__class__.__name__,
            "error.message": self.message,
            "error.code": self.code,
        }

        # Add context with error prefix
        for key, value in self.context.items():
            # If key already has a prefix, use it; otherwise add error prefix
            if "." in key:
                result[key] = value
            else:
                result[f"error.{key}"] = value

        if self.cause:
            result["error.cause"] = str(None)
            result["error.cause_type"] = type(self.cause).__name__

        return result

    def xǁFoundationErrorǁto_dict__mutmut_16(self) -> dict[str, Any]:
        """Convert exception to dictionary for structured logging.

        Returns:
            Dictionary representation suitable for logging/serialization.

        """
        result = {
            "error.type": self.__class__.__name__,
            "error.message": self.message,
            "error.code": self.code,
        }

        # Add context with error prefix
        for key, value in self.context.items():
            # If key already has a prefix, use it; otherwise add error prefix
            if "." in key:
                result[key] = value
            else:
                result[f"error.{key}"] = value

        if self.cause:
            result["error.cause"] = str(self.cause)
            result["error.cause_type"] = None

        return result

    def xǁFoundationErrorǁto_dict__mutmut_17(self) -> dict[str, Any]:
        """Convert exception to dictionary for structured logging.

        Returns:
            Dictionary representation suitable for logging/serialization.

        """
        result = {
            "error.type": self.__class__.__name__,
            "error.message": self.message,
            "error.code": self.code,
        }

        # Add context with error prefix
        for key, value in self.context.items():
            # If key already has a prefix, use it; otherwise add error prefix
            if "." in key:
                result[key] = value
            else:
                result[f"error.{key}"] = value

        if self.cause:
            result["error.cause"] = str(self.cause)
            result["XXerror.cause_typeXX"] = type(self.cause).__name__

        return result

    def xǁFoundationErrorǁto_dict__mutmut_18(self) -> dict[str, Any]:
        """Convert exception to dictionary for structured logging.

        Returns:
            Dictionary representation suitable for logging/serialization.

        """
        result = {
            "error.type": self.__class__.__name__,
            "error.message": self.message,
            "error.code": self.code,
        }

        # Add context with error prefix
        for key, value in self.context.items():
            # If key already has a prefix, use it; otherwise add error prefix
            if "." in key:
                result[key] = value
            else:
                result[f"error.{key}"] = value

        if self.cause:
            result["error.cause"] = str(self.cause)
            result["ERROR.CAUSE_TYPE"] = type(self.cause).__name__

        return result

    def xǁFoundationErrorǁto_dict__mutmut_19(self) -> dict[str, Any]:
        """Convert exception to dictionary for structured logging.

        Returns:
            Dictionary representation suitable for logging/serialization.

        """
        result = {
            "error.type": self.__class__.__name__,
            "error.message": self.message,
            "error.code": self.code,
        }

        # Add context with error prefix
        for key, value in self.context.items():
            # If key already has a prefix, use it; otherwise add error prefix
            if "." in key:
                result[key] = value
            else:
                result[f"error.{key}"] = value

        if self.cause:
            result["error.cause"] = str(self.cause)
            result["error.cause_type"] = type(None).__name__

        return result
    
    xǁFoundationErrorǁto_dict__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFoundationErrorǁto_dict__mutmut_1': xǁFoundationErrorǁto_dict__mutmut_1, 
        'xǁFoundationErrorǁto_dict__mutmut_2': xǁFoundationErrorǁto_dict__mutmut_2, 
        'xǁFoundationErrorǁto_dict__mutmut_3': xǁFoundationErrorǁto_dict__mutmut_3, 
        'xǁFoundationErrorǁto_dict__mutmut_4': xǁFoundationErrorǁto_dict__mutmut_4, 
        'xǁFoundationErrorǁto_dict__mutmut_5': xǁFoundationErrorǁto_dict__mutmut_5, 
        'xǁFoundationErrorǁto_dict__mutmut_6': xǁFoundationErrorǁto_dict__mutmut_6, 
        'xǁFoundationErrorǁto_dict__mutmut_7': xǁFoundationErrorǁto_dict__mutmut_7, 
        'xǁFoundationErrorǁto_dict__mutmut_8': xǁFoundationErrorǁto_dict__mutmut_8, 
        'xǁFoundationErrorǁto_dict__mutmut_9': xǁFoundationErrorǁto_dict__mutmut_9, 
        'xǁFoundationErrorǁto_dict__mutmut_10': xǁFoundationErrorǁto_dict__mutmut_10, 
        'xǁFoundationErrorǁto_dict__mutmut_11': xǁFoundationErrorǁto_dict__mutmut_11, 
        'xǁFoundationErrorǁto_dict__mutmut_12': xǁFoundationErrorǁto_dict__mutmut_12, 
        'xǁFoundationErrorǁto_dict__mutmut_13': xǁFoundationErrorǁto_dict__mutmut_13, 
        'xǁFoundationErrorǁto_dict__mutmut_14': xǁFoundationErrorǁto_dict__mutmut_14, 
        'xǁFoundationErrorǁto_dict__mutmut_15': xǁFoundationErrorǁto_dict__mutmut_15, 
        'xǁFoundationErrorǁto_dict__mutmut_16': xǁFoundationErrorǁto_dict__mutmut_16, 
        'xǁFoundationErrorǁto_dict__mutmut_17': xǁFoundationErrorǁto_dict__mutmut_17, 
        'xǁFoundationErrorǁto_dict__mutmut_18': xǁFoundationErrorǁto_dict__mutmut_18, 
        'xǁFoundationErrorǁto_dict__mutmut_19': xǁFoundationErrorǁto_dict__mutmut_19
    }
    
    def to_dict(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFoundationErrorǁto_dict__mutmut_orig"), object.__getattribute__(self, "xǁFoundationErrorǁto_dict__mutmut_mutants"), args, kwargs, self)
        return result 
    
    to_dict.__signature__ = _mutmut_signature(xǁFoundationErrorǁto_dict__mutmut_orig)
    xǁFoundationErrorǁto_dict__mutmut_orig.__name__ = 'xǁFoundationErrorǁto_dict'


# <3 🧱🤝🐛🪄
