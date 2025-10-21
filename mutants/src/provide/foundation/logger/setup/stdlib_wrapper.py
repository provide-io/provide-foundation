# provide/foundation/logger/setup/stdlib_wrapper.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import logging as stdlib_logging
from typing import Any

"""Wrapper for stdlib logger to accept structlog-style kwargs."""
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


class StructuredStdlibLogger:
    """Wrapper around stdlib logger that accepts structlog-style kwargs."""

    def xǁStructuredStdlibLoggerǁ__init____mutmut_orig(self, logger: Any) -> None:
        """Initialize with a stdlib logger instance."""
        self._logger = logger

    def xǁStructuredStdlibLoggerǁ__init____mutmut_1(self, logger: Any) -> None:
        """Initialize with a stdlib logger instance."""
        self._logger = None
    
    xǁStructuredStdlibLoggerǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStructuredStdlibLoggerǁ__init____mutmut_1': xǁStructuredStdlibLoggerǁ__init____mutmut_1
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStructuredStdlibLoggerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁStructuredStdlibLoggerǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁStructuredStdlibLoggerǁ__init____mutmut_orig)
    xǁStructuredStdlibLoggerǁ__init____mutmut_orig.__name__ = 'xǁStructuredStdlibLoggerǁ__init__'

    def xǁStructuredStdlibLoggerǁ_log__mutmut_orig(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_1(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = None
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_2(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = None

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_3(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = None

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_4(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"XXexc_infoXX", "stack_info", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_5(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"EXC_INFO", "stack_info", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_6(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "XXstack_infoXX", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_7(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "STACK_INFO", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_8(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "XXstacklevelXX", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_9(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "STACKLEVEL", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_10(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "stacklevel", "XXextraXX"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_11(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "stacklevel", "EXTRA"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_12(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key not in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_13(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = None
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_14(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = None

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_15(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "XXextraXX" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_16(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "EXTRA" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_17(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" not in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_18(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(None)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_19(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["XXextraXX"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_20(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["EXTRA"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_21(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = None

        self._logger.log(level, msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_22(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["XXextraXX"] = extra_dict

        self._logger.log(level, msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_23(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["EXTRA"] = extra_dict

        self._logger.log(level, msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_24(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(None, msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_25(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, None, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_26(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(msg, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_27(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, *args, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_28(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, msg, **stdlib_kwargs)

    def xǁStructuredStdlibLoggerǁ_log__mutmut_29(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method that converts kwargs to extra dict."""
        # Separate stdlib logging kwargs from structured logging kwargs
        stdlib_kwargs = {}
        extra_dict = {}

        # Known stdlib logging kwargs
        stdlib_params = {"exc_info", "stack_info", "stacklevel", "extra"}

        for key, value in kwargs.items():
            if key in stdlib_params:
                stdlib_kwargs[key] = value
            else:
                # These are structured logging key-value pairs
                extra_dict[key] = value

        # Merge any existing extra dict
        if "extra" in stdlib_kwargs:
            stdlib_kwargs["extra"].update(extra_dict)
        elif extra_dict:
            stdlib_kwargs["extra"] = extra_dict

        self._logger.log(level, msg, *args, )
    
    xǁStructuredStdlibLoggerǁ_log__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStructuredStdlibLoggerǁ_log__mutmut_1': xǁStructuredStdlibLoggerǁ_log__mutmut_1, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_2': xǁStructuredStdlibLoggerǁ_log__mutmut_2, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_3': xǁStructuredStdlibLoggerǁ_log__mutmut_3, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_4': xǁStructuredStdlibLoggerǁ_log__mutmut_4, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_5': xǁStructuredStdlibLoggerǁ_log__mutmut_5, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_6': xǁStructuredStdlibLoggerǁ_log__mutmut_6, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_7': xǁStructuredStdlibLoggerǁ_log__mutmut_7, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_8': xǁStructuredStdlibLoggerǁ_log__mutmut_8, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_9': xǁStructuredStdlibLoggerǁ_log__mutmut_9, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_10': xǁStructuredStdlibLoggerǁ_log__mutmut_10, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_11': xǁStructuredStdlibLoggerǁ_log__mutmut_11, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_12': xǁStructuredStdlibLoggerǁ_log__mutmut_12, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_13': xǁStructuredStdlibLoggerǁ_log__mutmut_13, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_14': xǁStructuredStdlibLoggerǁ_log__mutmut_14, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_15': xǁStructuredStdlibLoggerǁ_log__mutmut_15, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_16': xǁStructuredStdlibLoggerǁ_log__mutmut_16, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_17': xǁStructuredStdlibLoggerǁ_log__mutmut_17, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_18': xǁStructuredStdlibLoggerǁ_log__mutmut_18, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_19': xǁStructuredStdlibLoggerǁ_log__mutmut_19, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_20': xǁStructuredStdlibLoggerǁ_log__mutmut_20, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_21': xǁStructuredStdlibLoggerǁ_log__mutmut_21, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_22': xǁStructuredStdlibLoggerǁ_log__mutmut_22, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_23': xǁStructuredStdlibLoggerǁ_log__mutmut_23, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_24': xǁStructuredStdlibLoggerǁ_log__mutmut_24, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_25': xǁStructuredStdlibLoggerǁ_log__mutmut_25, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_26': xǁStructuredStdlibLoggerǁ_log__mutmut_26, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_27': xǁStructuredStdlibLoggerǁ_log__mutmut_27, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_28': xǁStructuredStdlibLoggerǁ_log__mutmut_28, 
        'xǁStructuredStdlibLoggerǁ_log__mutmut_29': xǁStructuredStdlibLoggerǁ_log__mutmut_29
    }
    
    def _log(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStructuredStdlibLoggerǁ_log__mutmut_orig"), object.__getattribute__(self, "xǁStructuredStdlibLoggerǁ_log__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _log.__signature__ = _mutmut_signature(xǁStructuredStdlibLoggerǁ_log__mutmut_orig)
    xǁStructuredStdlibLoggerǁ_log__mutmut_orig.__name__ = 'xǁStructuredStdlibLoggerǁ_log'

    def xǁStructuredStdlibLoggerǁdebug__mutmut_orig(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at DEBUG level with structured kwargs."""
        self._log(stdlib_logging.DEBUG, msg, *args, **kwargs)

    def xǁStructuredStdlibLoggerǁdebug__mutmut_1(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at DEBUG level with structured kwargs."""
        self._log(None, msg, *args, **kwargs)

    def xǁStructuredStdlibLoggerǁdebug__mutmut_2(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at DEBUG level with structured kwargs."""
        self._log(stdlib_logging.DEBUG, None, *args, **kwargs)

    def xǁStructuredStdlibLoggerǁdebug__mutmut_3(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at DEBUG level with structured kwargs."""
        self._log(msg, *args, **kwargs)

    def xǁStructuredStdlibLoggerǁdebug__mutmut_4(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at DEBUG level with structured kwargs."""
        self._log(stdlib_logging.DEBUG, *args, **kwargs)

    def xǁStructuredStdlibLoggerǁdebug__mutmut_5(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at DEBUG level with structured kwargs."""
        self._log(stdlib_logging.DEBUG, msg, **kwargs)

    def xǁStructuredStdlibLoggerǁdebug__mutmut_6(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at DEBUG level with structured kwargs."""
        self._log(stdlib_logging.DEBUG, msg, *args, )
    
    xǁStructuredStdlibLoggerǁdebug__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStructuredStdlibLoggerǁdebug__mutmut_1': xǁStructuredStdlibLoggerǁdebug__mutmut_1, 
        'xǁStructuredStdlibLoggerǁdebug__mutmut_2': xǁStructuredStdlibLoggerǁdebug__mutmut_2, 
        'xǁStructuredStdlibLoggerǁdebug__mutmut_3': xǁStructuredStdlibLoggerǁdebug__mutmut_3, 
        'xǁStructuredStdlibLoggerǁdebug__mutmut_4': xǁStructuredStdlibLoggerǁdebug__mutmut_4, 
        'xǁStructuredStdlibLoggerǁdebug__mutmut_5': xǁStructuredStdlibLoggerǁdebug__mutmut_5, 
        'xǁStructuredStdlibLoggerǁdebug__mutmut_6': xǁStructuredStdlibLoggerǁdebug__mutmut_6
    }
    
    def debug(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStructuredStdlibLoggerǁdebug__mutmut_orig"), object.__getattribute__(self, "xǁStructuredStdlibLoggerǁdebug__mutmut_mutants"), args, kwargs, self)
        return result 
    
    debug.__signature__ = _mutmut_signature(xǁStructuredStdlibLoggerǁdebug__mutmut_orig)
    xǁStructuredStdlibLoggerǁdebug__mutmut_orig.__name__ = 'xǁStructuredStdlibLoggerǁdebug'

    def xǁStructuredStdlibLoggerǁinfo__mutmut_orig(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at INFO level with structured kwargs."""
        self._log(stdlib_logging.INFO, msg, *args, **kwargs)

    def xǁStructuredStdlibLoggerǁinfo__mutmut_1(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at INFO level with structured kwargs."""
        self._log(None, msg, *args, **kwargs)

    def xǁStructuredStdlibLoggerǁinfo__mutmut_2(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at INFO level with structured kwargs."""
        self._log(stdlib_logging.INFO, None, *args, **kwargs)

    def xǁStructuredStdlibLoggerǁinfo__mutmut_3(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at INFO level with structured kwargs."""
        self._log(msg, *args, **kwargs)

    def xǁStructuredStdlibLoggerǁinfo__mutmut_4(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at INFO level with structured kwargs."""
        self._log(stdlib_logging.INFO, *args, **kwargs)

    def xǁStructuredStdlibLoggerǁinfo__mutmut_5(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at INFO level with structured kwargs."""
        self._log(stdlib_logging.INFO, msg, **kwargs)

    def xǁStructuredStdlibLoggerǁinfo__mutmut_6(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at INFO level with structured kwargs."""
        self._log(stdlib_logging.INFO, msg, *args, )
    
    xǁStructuredStdlibLoggerǁinfo__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStructuredStdlibLoggerǁinfo__mutmut_1': xǁStructuredStdlibLoggerǁinfo__mutmut_1, 
        'xǁStructuredStdlibLoggerǁinfo__mutmut_2': xǁStructuredStdlibLoggerǁinfo__mutmut_2, 
        'xǁStructuredStdlibLoggerǁinfo__mutmut_3': xǁStructuredStdlibLoggerǁinfo__mutmut_3, 
        'xǁStructuredStdlibLoggerǁinfo__mutmut_4': xǁStructuredStdlibLoggerǁinfo__mutmut_4, 
        'xǁStructuredStdlibLoggerǁinfo__mutmut_5': xǁStructuredStdlibLoggerǁinfo__mutmut_5, 
        'xǁStructuredStdlibLoggerǁinfo__mutmut_6': xǁStructuredStdlibLoggerǁinfo__mutmut_6
    }
    
    def info(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStructuredStdlibLoggerǁinfo__mutmut_orig"), object.__getattribute__(self, "xǁStructuredStdlibLoggerǁinfo__mutmut_mutants"), args, kwargs, self)
        return result 
    
    info.__signature__ = _mutmut_signature(xǁStructuredStdlibLoggerǁinfo__mutmut_orig)
    xǁStructuredStdlibLoggerǁinfo__mutmut_orig.__name__ = 'xǁStructuredStdlibLoggerǁinfo'

    def xǁStructuredStdlibLoggerǁwarning__mutmut_orig(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at WARNING level with structured kwargs."""
        self._log(stdlib_logging.WARNING, msg, *args, **kwargs)

    def xǁStructuredStdlibLoggerǁwarning__mutmut_1(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at WARNING level with structured kwargs."""
        self._log(None, msg, *args, **kwargs)

    def xǁStructuredStdlibLoggerǁwarning__mutmut_2(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at WARNING level with structured kwargs."""
        self._log(stdlib_logging.WARNING, None, *args, **kwargs)

    def xǁStructuredStdlibLoggerǁwarning__mutmut_3(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at WARNING level with structured kwargs."""
        self._log(msg, *args, **kwargs)

    def xǁStructuredStdlibLoggerǁwarning__mutmut_4(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at WARNING level with structured kwargs."""
        self._log(stdlib_logging.WARNING, *args, **kwargs)

    def xǁStructuredStdlibLoggerǁwarning__mutmut_5(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at WARNING level with structured kwargs."""
        self._log(stdlib_logging.WARNING, msg, **kwargs)

    def xǁStructuredStdlibLoggerǁwarning__mutmut_6(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at WARNING level with structured kwargs."""
        self._log(stdlib_logging.WARNING, msg, *args, )
    
    xǁStructuredStdlibLoggerǁwarning__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStructuredStdlibLoggerǁwarning__mutmut_1': xǁStructuredStdlibLoggerǁwarning__mutmut_1, 
        'xǁStructuredStdlibLoggerǁwarning__mutmut_2': xǁStructuredStdlibLoggerǁwarning__mutmut_2, 
        'xǁStructuredStdlibLoggerǁwarning__mutmut_3': xǁStructuredStdlibLoggerǁwarning__mutmut_3, 
        'xǁStructuredStdlibLoggerǁwarning__mutmut_4': xǁStructuredStdlibLoggerǁwarning__mutmut_4, 
        'xǁStructuredStdlibLoggerǁwarning__mutmut_5': xǁStructuredStdlibLoggerǁwarning__mutmut_5, 
        'xǁStructuredStdlibLoggerǁwarning__mutmut_6': xǁStructuredStdlibLoggerǁwarning__mutmut_6
    }
    
    def warning(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStructuredStdlibLoggerǁwarning__mutmut_orig"), object.__getattribute__(self, "xǁStructuredStdlibLoggerǁwarning__mutmut_mutants"), args, kwargs, self)
        return result 
    
    warning.__signature__ = _mutmut_signature(xǁStructuredStdlibLoggerǁwarning__mutmut_orig)
    xǁStructuredStdlibLoggerǁwarning__mutmut_orig.__name__ = 'xǁStructuredStdlibLoggerǁwarning'

    def xǁStructuredStdlibLoggerǁerror__mutmut_orig(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at ERROR level with structured kwargs."""
        self._log(stdlib_logging.ERROR, msg, *args, **kwargs)

    def xǁStructuredStdlibLoggerǁerror__mutmut_1(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at ERROR level with structured kwargs."""
        self._log(None, msg, *args, **kwargs)

    def xǁStructuredStdlibLoggerǁerror__mutmut_2(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at ERROR level with structured kwargs."""
        self._log(stdlib_logging.ERROR, None, *args, **kwargs)

    def xǁStructuredStdlibLoggerǁerror__mutmut_3(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at ERROR level with structured kwargs."""
        self._log(msg, *args, **kwargs)

    def xǁStructuredStdlibLoggerǁerror__mutmut_4(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at ERROR level with structured kwargs."""
        self._log(stdlib_logging.ERROR, *args, **kwargs)

    def xǁStructuredStdlibLoggerǁerror__mutmut_5(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at ERROR level with structured kwargs."""
        self._log(stdlib_logging.ERROR, msg, **kwargs)

    def xǁStructuredStdlibLoggerǁerror__mutmut_6(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at ERROR level with structured kwargs."""
        self._log(stdlib_logging.ERROR, msg, *args, )
    
    xǁStructuredStdlibLoggerǁerror__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStructuredStdlibLoggerǁerror__mutmut_1': xǁStructuredStdlibLoggerǁerror__mutmut_1, 
        'xǁStructuredStdlibLoggerǁerror__mutmut_2': xǁStructuredStdlibLoggerǁerror__mutmut_2, 
        'xǁStructuredStdlibLoggerǁerror__mutmut_3': xǁStructuredStdlibLoggerǁerror__mutmut_3, 
        'xǁStructuredStdlibLoggerǁerror__mutmut_4': xǁStructuredStdlibLoggerǁerror__mutmut_4, 
        'xǁStructuredStdlibLoggerǁerror__mutmut_5': xǁStructuredStdlibLoggerǁerror__mutmut_5, 
        'xǁStructuredStdlibLoggerǁerror__mutmut_6': xǁStructuredStdlibLoggerǁerror__mutmut_6
    }
    
    def error(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStructuredStdlibLoggerǁerror__mutmut_orig"), object.__getattribute__(self, "xǁStructuredStdlibLoggerǁerror__mutmut_mutants"), args, kwargs, self)
        return result 
    
    error.__signature__ = _mutmut_signature(xǁStructuredStdlibLoggerǁerror__mutmut_orig)
    xǁStructuredStdlibLoggerǁerror__mutmut_orig.__name__ = 'xǁStructuredStdlibLoggerǁerror'

    def xǁStructuredStdlibLoggerǁcritical__mutmut_orig(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at CRITICAL level with structured kwargs."""
        self._log(stdlib_logging.CRITICAL, msg, *args, **kwargs)

    def xǁStructuredStdlibLoggerǁcritical__mutmut_1(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at CRITICAL level with structured kwargs."""
        self._log(None, msg, *args, **kwargs)

    def xǁStructuredStdlibLoggerǁcritical__mutmut_2(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at CRITICAL level with structured kwargs."""
        self._log(stdlib_logging.CRITICAL, None, *args, **kwargs)

    def xǁStructuredStdlibLoggerǁcritical__mutmut_3(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at CRITICAL level with structured kwargs."""
        self._log(msg, *args, **kwargs)

    def xǁStructuredStdlibLoggerǁcritical__mutmut_4(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at CRITICAL level with structured kwargs."""
        self._log(stdlib_logging.CRITICAL, *args, **kwargs)

    def xǁStructuredStdlibLoggerǁcritical__mutmut_5(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at CRITICAL level with structured kwargs."""
        self._log(stdlib_logging.CRITICAL, msg, **kwargs)

    def xǁStructuredStdlibLoggerǁcritical__mutmut_6(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log at CRITICAL level with structured kwargs."""
        self._log(stdlib_logging.CRITICAL, msg, *args, )
    
    xǁStructuredStdlibLoggerǁcritical__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁStructuredStdlibLoggerǁcritical__mutmut_1': xǁStructuredStdlibLoggerǁcritical__mutmut_1, 
        'xǁStructuredStdlibLoggerǁcritical__mutmut_2': xǁStructuredStdlibLoggerǁcritical__mutmut_2, 
        'xǁStructuredStdlibLoggerǁcritical__mutmut_3': xǁStructuredStdlibLoggerǁcritical__mutmut_3, 
        'xǁStructuredStdlibLoggerǁcritical__mutmut_4': xǁStructuredStdlibLoggerǁcritical__mutmut_4, 
        'xǁStructuredStdlibLoggerǁcritical__mutmut_5': xǁStructuredStdlibLoggerǁcritical__mutmut_5, 
        'xǁStructuredStdlibLoggerǁcritical__mutmut_6': xǁStructuredStdlibLoggerǁcritical__mutmut_6
    }
    
    def critical(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁStructuredStdlibLoggerǁcritical__mutmut_orig"), object.__getattribute__(self, "xǁStructuredStdlibLoggerǁcritical__mutmut_mutants"), args, kwargs, self)
        return result 
    
    critical.__signature__ = _mutmut_signature(xǁStructuredStdlibLoggerǁcritical__mutmut_orig)
    xǁStructuredStdlibLoggerǁcritical__mutmut_orig.__name__ = 'xǁStructuredStdlibLoggerǁcritical'


__all__ = ["StructuredStdlibLogger"]


# <3 🧱🤝📝🪄
