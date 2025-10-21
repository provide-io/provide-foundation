# provide/foundation/errors/safe_decorators.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from collections.abc import Callable
import functools
import inspect
from typing import Any, TypeVar

from provide.foundation.hub.foundation import get_foundation_logger

"""Safe error decorators that preserve original behavior."""

F = TypeVar("F", bound=Callable[..., Any])
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


def x__get_func_name__mutmut_orig(func: Callable) -> str:
    """Get function name with fallback."""
    return getattr(func, "__name__", "<anonymous>")


def x__get_func_name__mutmut_1(func: Callable) -> str:
    """Get function name with fallback."""
    return getattr(None, "__name__", "<anonymous>")


def x__get_func_name__mutmut_2(func: Callable) -> str:
    """Get function name with fallback."""
    return getattr(func, None, "<anonymous>")


def x__get_func_name__mutmut_3(func: Callable) -> str:
    """Get function name with fallback."""
    return getattr(func, "__name__", None)


def x__get_func_name__mutmut_4(func: Callable) -> str:
    """Get function name with fallback."""
    return getattr("__name__", "<anonymous>")


def x__get_func_name__mutmut_5(func: Callable) -> str:
    """Get function name with fallback."""
    return getattr(func, "<anonymous>")


def x__get_func_name__mutmut_6(func: Callable) -> str:
    """Get function name with fallback."""
    return getattr(func, "__name__", )


def x__get_func_name__mutmut_7(func: Callable) -> str:
    """Get function name with fallback."""
    return getattr(func, "XX__name__XX", "<anonymous>")


def x__get_func_name__mutmut_8(func: Callable) -> str:
    """Get function name with fallback."""
    return getattr(func, "__NAME__", "<anonymous>")


def x__get_func_name__mutmut_9(func: Callable) -> str:
    """Get function name with fallback."""
    return getattr(func, "__name__", "XX<anonymous>XX")


def x__get_func_name__mutmut_10(func: Callable) -> str:
    """Get function name with fallback."""
    return getattr(func, "__name__", "<ANONYMOUS>")

x__get_func_name__mutmut_mutants : ClassVar[MutantDict] = {
'x__get_func_name__mutmut_1': x__get_func_name__mutmut_1, 
    'x__get_func_name__mutmut_2': x__get_func_name__mutmut_2, 
    'x__get_func_name__mutmut_3': x__get_func_name__mutmut_3, 
    'x__get_func_name__mutmut_4': x__get_func_name__mutmut_4, 
    'x__get_func_name__mutmut_5': x__get_func_name__mutmut_5, 
    'x__get_func_name__mutmut_6': x__get_func_name__mutmut_6, 
    'x__get_func_name__mutmut_7': x__get_func_name__mutmut_7, 
    'x__get_func_name__mutmut_8': x__get_func_name__mutmut_8, 
    'x__get_func_name__mutmut_9': x__get_func_name__mutmut_9, 
    'x__get_func_name__mutmut_10': x__get_func_name__mutmut_10
}

def _get_func_name(*args, **kwargs):
    result = _mutmut_trampoline(x__get_func_name__mutmut_orig, x__get_func_name__mutmut_mutants, args, kwargs)
    return result 

_get_func_name.__signature__ = _mutmut_signature(x__get_func_name__mutmut_orig)
x__get_func_name__mutmut_orig.__name__ = 'x__get_func_name'


def x__log_function_entry__mutmut_orig(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log function entry if appropriate level."""
    if log_level in ("debug", "trace"):
        log_method = getattr(logger, log_level)
        func_name = _get_func_name(func)
        log_method(
            f"Entering {func_name}",
            function=func_name,
            **context,
        )


def x__log_function_entry__mutmut_1(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log function entry if appropriate level."""
    if log_level not in ("debug", "trace"):
        log_method = getattr(logger, log_level)
        func_name = _get_func_name(func)
        log_method(
            f"Entering {func_name}",
            function=func_name,
            **context,
        )


def x__log_function_entry__mutmut_2(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log function entry if appropriate level."""
    if log_level in ("XXdebugXX", "trace"):
        log_method = getattr(logger, log_level)
        func_name = _get_func_name(func)
        log_method(
            f"Entering {func_name}",
            function=func_name,
            **context,
        )


def x__log_function_entry__mutmut_3(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log function entry if appropriate level."""
    if log_level in ("DEBUG", "trace"):
        log_method = getattr(logger, log_level)
        func_name = _get_func_name(func)
        log_method(
            f"Entering {func_name}",
            function=func_name,
            **context,
        )


def x__log_function_entry__mutmut_4(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log function entry if appropriate level."""
    if log_level in ("debug", "XXtraceXX"):
        log_method = getattr(logger, log_level)
        func_name = _get_func_name(func)
        log_method(
            f"Entering {func_name}",
            function=func_name,
            **context,
        )


def x__log_function_entry__mutmut_5(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log function entry if appropriate level."""
    if log_level in ("debug", "TRACE"):
        log_method = getattr(logger, log_level)
        func_name = _get_func_name(func)
        log_method(
            f"Entering {func_name}",
            function=func_name,
            **context,
        )


def x__log_function_entry__mutmut_6(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log function entry if appropriate level."""
    if log_level in ("debug", "trace"):
        log_method = None
        func_name = _get_func_name(func)
        log_method(
            f"Entering {func_name}",
            function=func_name,
            **context,
        )


def x__log_function_entry__mutmut_7(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log function entry if appropriate level."""
    if log_level in ("debug", "trace"):
        log_method = getattr(None, log_level)
        func_name = _get_func_name(func)
        log_method(
            f"Entering {func_name}",
            function=func_name,
            **context,
        )


def x__log_function_entry__mutmut_8(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log function entry if appropriate level."""
    if log_level in ("debug", "trace"):
        log_method = getattr(logger, None)
        func_name = _get_func_name(func)
        log_method(
            f"Entering {func_name}",
            function=func_name,
            **context,
        )


def x__log_function_entry__mutmut_9(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log function entry if appropriate level."""
    if log_level in ("debug", "trace"):
        log_method = getattr(log_level)
        func_name = _get_func_name(func)
        log_method(
            f"Entering {func_name}",
            function=func_name,
            **context,
        )


def x__log_function_entry__mutmut_10(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log function entry if appropriate level."""
    if log_level in ("debug", "trace"):
        log_method = getattr(logger, )
        func_name = _get_func_name(func)
        log_method(
            f"Entering {func_name}",
            function=func_name,
            **context,
        )


def x__log_function_entry__mutmut_11(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log function entry if appropriate level."""
    if log_level in ("debug", "trace"):
        log_method = getattr(logger, log_level)
        func_name = None
        log_method(
            f"Entering {func_name}",
            function=func_name,
            **context,
        )


def x__log_function_entry__mutmut_12(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log function entry if appropriate level."""
    if log_level in ("debug", "trace"):
        log_method = getattr(logger, log_level)
        func_name = _get_func_name(None)
        log_method(
            f"Entering {func_name}",
            function=func_name,
            **context,
        )


def x__log_function_entry__mutmut_13(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log function entry if appropriate level."""
    if log_level in ("debug", "trace"):
        log_method = getattr(logger, log_level)
        func_name = _get_func_name(func)
        log_method(
            None,
            function=func_name,
            **context,
        )


def x__log_function_entry__mutmut_14(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log function entry if appropriate level."""
    if log_level in ("debug", "trace"):
        log_method = getattr(logger, log_level)
        func_name = _get_func_name(func)
        log_method(
            f"Entering {func_name}",
            function=None,
            **context,
        )


def x__log_function_entry__mutmut_15(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log function entry if appropriate level."""
    if log_level in ("debug", "trace"):
        log_method = getattr(logger, log_level)
        func_name = _get_func_name(func)
        log_method(
            function=func_name,
            **context,
        )


def x__log_function_entry__mutmut_16(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log function entry if appropriate level."""
    if log_level in ("debug", "trace"):
        log_method = getattr(logger, log_level)
        func_name = _get_func_name(func)
        log_method(
            f"Entering {func_name}",
            **context,
        )


def x__log_function_entry__mutmut_17(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log function entry if appropriate level."""
    if log_level in ("debug", "trace"):
        log_method = getattr(logger, log_level)
        func_name = _get_func_name(func)
        log_method(
            f"Entering {func_name}",
            function=func_name,
            )

x__log_function_entry__mutmut_mutants : ClassVar[MutantDict] = {
'x__log_function_entry__mutmut_1': x__log_function_entry__mutmut_1, 
    'x__log_function_entry__mutmut_2': x__log_function_entry__mutmut_2, 
    'x__log_function_entry__mutmut_3': x__log_function_entry__mutmut_3, 
    'x__log_function_entry__mutmut_4': x__log_function_entry__mutmut_4, 
    'x__log_function_entry__mutmut_5': x__log_function_entry__mutmut_5, 
    'x__log_function_entry__mutmut_6': x__log_function_entry__mutmut_6, 
    'x__log_function_entry__mutmut_7': x__log_function_entry__mutmut_7, 
    'x__log_function_entry__mutmut_8': x__log_function_entry__mutmut_8, 
    'x__log_function_entry__mutmut_9': x__log_function_entry__mutmut_9, 
    'x__log_function_entry__mutmut_10': x__log_function_entry__mutmut_10, 
    'x__log_function_entry__mutmut_11': x__log_function_entry__mutmut_11, 
    'x__log_function_entry__mutmut_12': x__log_function_entry__mutmut_12, 
    'x__log_function_entry__mutmut_13': x__log_function_entry__mutmut_13, 
    'x__log_function_entry__mutmut_14': x__log_function_entry__mutmut_14, 
    'x__log_function_entry__mutmut_15': x__log_function_entry__mutmut_15, 
    'x__log_function_entry__mutmut_16': x__log_function_entry__mutmut_16, 
    'x__log_function_entry__mutmut_17': x__log_function_entry__mutmut_17
}

def _log_function_entry(*args, **kwargs):
    result = _mutmut_trampoline(x__log_function_entry__mutmut_orig, x__log_function_entry__mutmut_mutants, args, kwargs)
    return result 

_log_function_entry.__signature__ = _mutmut_signature(x__log_function_entry__mutmut_orig)
x__log_function_entry__mutmut_orig.__name__ = 'x__log_function_entry'


def x__log_function_success__mutmut_orig(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log successful function completion."""
    log_method = getattr(logger, log_level, logger.debug)
    func_name = _get_func_name(func)
    log_method(
        f"Successfully completed {func_name}",
        function=func_name,
        **context,
    )


def x__log_function_success__mutmut_1(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log successful function completion."""
    log_method = None
    func_name = _get_func_name(func)
    log_method(
        f"Successfully completed {func_name}",
        function=func_name,
        **context,
    )


def x__log_function_success__mutmut_2(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log successful function completion."""
    log_method = getattr(None, log_level, logger.debug)
    func_name = _get_func_name(func)
    log_method(
        f"Successfully completed {func_name}",
        function=func_name,
        **context,
    )


def x__log_function_success__mutmut_3(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log successful function completion."""
    log_method = getattr(logger, None, logger.debug)
    func_name = _get_func_name(func)
    log_method(
        f"Successfully completed {func_name}",
        function=func_name,
        **context,
    )


def x__log_function_success__mutmut_4(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log successful function completion."""
    log_method = getattr(logger, log_level, None)
    func_name = _get_func_name(func)
    log_method(
        f"Successfully completed {func_name}",
        function=func_name,
        **context,
    )


def x__log_function_success__mutmut_5(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log successful function completion."""
    log_method = getattr(log_level, logger.debug)
    func_name = _get_func_name(func)
    log_method(
        f"Successfully completed {func_name}",
        function=func_name,
        **context,
    )


def x__log_function_success__mutmut_6(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log successful function completion."""
    log_method = getattr(logger, logger.debug)
    func_name = _get_func_name(func)
    log_method(
        f"Successfully completed {func_name}",
        function=func_name,
        **context,
    )


def x__log_function_success__mutmut_7(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log successful function completion."""
    log_method = getattr(logger, log_level, )
    func_name = _get_func_name(func)
    log_method(
        f"Successfully completed {func_name}",
        function=func_name,
        **context,
    )


def x__log_function_success__mutmut_8(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log successful function completion."""
    log_method = getattr(logger, log_level, logger.debug)
    func_name = None
    log_method(
        f"Successfully completed {func_name}",
        function=func_name,
        **context,
    )


def x__log_function_success__mutmut_9(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log successful function completion."""
    log_method = getattr(logger, log_level, logger.debug)
    func_name = _get_func_name(None)
    log_method(
        f"Successfully completed {func_name}",
        function=func_name,
        **context,
    )


def x__log_function_success__mutmut_10(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log successful function completion."""
    log_method = getattr(logger, log_level, logger.debug)
    func_name = _get_func_name(func)
    log_method(
        None,
        function=func_name,
        **context,
    )


def x__log_function_success__mutmut_11(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log successful function completion."""
    log_method = getattr(logger, log_level, logger.debug)
    func_name = _get_func_name(func)
    log_method(
        f"Successfully completed {func_name}",
        function=None,
        **context,
    )


def x__log_function_success__mutmut_12(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log successful function completion."""
    log_method = getattr(logger, log_level, logger.debug)
    func_name = _get_func_name(func)
    log_method(
        function=func_name,
        **context,
    )


def x__log_function_success__mutmut_13(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log successful function completion."""
    log_method = getattr(logger, log_level, logger.debug)
    func_name = _get_func_name(func)
    log_method(
        f"Successfully completed {func_name}",
        **context,
    )


def x__log_function_success__mutmut_14(logger: Any, func: Callable, log_level: str, context: dict[str, Any]) -> None:
    """Log successful function completion."""
    log_method = getattr(logger, log_level, logger.debug)
    func_name = _get_func_name(func)
    log_method(
        f"Successfully completed {func_name}",
        function=func_name,
        )

x__log_function_success__mutmut_mutants : ClassVar[MutantDict] = {
'x__log_function_success__mutmut_1': x__log_function_success__mutmut_1, 
    'x__log_function_success__mutmut_2': x__log_function_success__mutmut_2, 
    'x__log_function_success__mutmut_3': x__log_function_success__mutmut_3, 
    'x__log_function_success__mutmut_4': x__log_function_success__mutmut_4, 
    'x__log_function_success__mutmut_5': x__log_function_success__mutmut_5, 
    'x__log_function_success__mutmut_6': x__log_function_success__mutmut_6, 
    'x__log_function_success__mutmut_7': x__log_function_success__mutmut_7, 
    'x__log_function_success__mutmut_8': x__log_function_success__mutmut_8, 
    'x__log_function_success__mutmut_9': x__log_function_success__mutmut_9, 
    'x__log_function_success__mutmut_10': x__log_function_success__mutmut_10, 
    'x__log_function_success__mutmut_11': x__log_function_success__mutmut_11, 
    'x__log_function_success__mutmut_12': x__log_function_success__mutmut_12, 
    'x__log_function_success__mutmut_13': x__log_function_success__mutmut_13, 
    'x__log_function_success__mutmut_14': x__log_function_success__mutmut_14
}

def _log_function_success(*args, **kwargs):
    result = _mutmut_trampoline(x__log_function_success__mutmut_orig, x__log_function_success__mutmut_mutants, args, kwargs)
    return result 

_log_function_success.__signature__ = _mutmut_signature(x__log_function_success__mutmut_orig)
x__log_function_success__mutmut_orig.__name__ = 'x__log_function_success'


def x__log_function_error__mutmut_orig(logger: Any, func: Callable, error: Exception, context: dict[str, Any]) -> None:
    """Log function error with context."""
    func_name = _get_func_name(func)
    logger.error(
        f"Error in {func_name}",
        exc_info=True,
        function=func_name,
        error_type=type(error).__name__,
        error_message=str(error),
        **context,
    )


def x__log_function_error__mutmut_1(logger: Any, func: Callable, error: Exception, context: dict[str, Any]) -> None:
    """Log function error with context."""
    func_name = None
    logger.error(
        f"Error in {func_name}",
        exc_info=True,
        function=func_name,
        error_type=type(error).__name__,
        error_message=str(error),
        **context,
    )


def x__log_function_error__mutmut_2(logger: Any, func: Callable, error: Exception, context: dict[str, Any]) -> None:
    """Log function error with context."""
    func_name = _get_func_name(None)
    logger.error(
        f"Error in {func_name}",
        exc_info=True,
        function=func_name,
        error_type=type(error).__name__,
        error_message=str(error),
        **context,
    )


def x__log_function_error__mutmut_3(logger: Any, func: Callable, error: Exception, context: dict[str, Any]) -> None:
    """Log function error with context."""
    func_name = _get_func_name(func)
    logger.error(
        None,
        exc_info=True,
        function=func_name,
        error_type=type(error).__name__,
        error_message=str(error),
        **context,
    )


def x__log_function_error__mutmut_4(logger: Any, func: Callable, error: Exception, context: dict[str, Any]) -> None:
    """Log function error with context."""
    func_name = _get_func_name(func)
    logger.error(
        f"Error in {func_name}",
        exc_info=None,
        function=func_name,
        error_type=type(error).__name__,
        error_message=str(error),
        **context,
    )


def x__log_function_error__mutmut_5(logger: Any, func: Callable, error: Exception, context: dict[str, Any]) -> None:
    """Log function error with context."""
    func_name = _get_func_name(func)
    logger.error(
        f"Error in {func_name}",
        exc_info=True,
        function=None,
        error_type=type(error).__name__,
        error_message=str(error),
        **context,
    )


def x__log_function_error__mutmut_6(logger: Any, func: Callable, error: Exception, context: dict[str, Any]) -> None:
    """Log function error with context."""
    func_name = _get_func_name(func)
    logger.error(
        f"Error in {func_name}",
        exc_info=True,
        function=func_name,
        error_type=None,
        error_message=str(error),
        **context,
    )


def x__log_function_error__mutmut_7(logger: Any, func: Callable, error: Exception, context: dict[str, Any]) -> None:
    """Log function error with context."""
    func_name = _get_func_name(func)
    logger.error(
        f"Error in {func_name}",
        exc_info=True,
        function=func_name,
        error_type=type(error).__name__,
        error_message=None,
        **context,
    )


def x__log_function_error__mutmut_8(logger: Any, func: Callable, error: Exception, context: dict[str, Any]) -> None:
    """Log function error with context."""
    func_name = _get_func_name(func)
    logger.error(
        exc_info=True,
        function=func_name,
        error_type=type(error).__name__,
        error_message=str(error),
        **context,
    )


def x__log_function_error__mutmut_9(logger: Any, func: Callable, error: Exception, context: dict[str, Any]) -> None:
    """Log function error with context."""
    func_name = _get_func_name(func)
    logger.error(
        f"Error in {func_name}",
        function=func_name,
        error_type=type(error).__name__,
        error_message=str(error),
        **context,
    )


def x__log_function_error__mutmut_10(logger: Any, func: Callable, error: Exception, context: dict[str, Any]) -> None:
    """Log function error with context."""
    func_name = _get_func_name(func)
    logger.error(
        f"Error in {func_name}",
        exc_info=True,
        error_type=type(error).__name__,
        error_message=str(error),
        **context,
    )


def x__log_function_error__mutmut_11(logger: Any, func: Callable, error: Exception, context: dict[str, Any]) -> None:
    """Log function error with context."""
    func_name = _get_func_name(func)
    logger.error(
        f"Error in {func_name}",
        exc_info=True,
        function=func_name,
        error_message=str(error),
        **context,
    )


def x__log_function_error__mutmut_12(logger: Any, func: Callable, error: Exception, context: dict[str, Any]) -> None:
    """Log function error with context."""
    func_name = _get_func_name(func)
    logger.error(
        f"Error in {func_name}",
        exc_info=True,
        function=func_name,
        error_type=type(error).__name__,
        **context,
    )


def x__log_function_error__mutmut_13(logger: Any, func: Callable, error: Exception, context: dict[str, Any]) -> None:
    """Log function error with context."""
    func_name = _get_func_name(func)
    logger.error(
        f"Error in {func_name}",
        exc_info=True,
        function=func_name,
        error_type=type(error).__name__,
        error_message=str(error),
        )


def x__log_function_error__mutmut_14(logger: Any, func: Callable, error: Exception, context: dict[str, Any]) -> None:
    """Log function error with context."""
    func_name = _get_func_name(func)
    logger.error(
        f"Error in {func_name}",
        exc_info=False,
        function=func_name,
        error_type=type(error).__name__,
        error_message=str(error),
        **context,
    )


def x__log_function_error__mutmut_15(logger: Any, func: Callable, error: Exception, context: dict[str, Any]) -> None:
    """Log function error with context."""
    func_name = _get_func_name(func)
    logger.error(
        f"Error in {func_name}",
        exc_info=True,
        function=func_name,
        error_type=type(None).__name__,
        error_message=str(error),
        **context,
    )


def x__log_function_error__mutmut_16(logger: Any, func: Callable, error: Exception, context: dict[str, Any]) -> None:
    """Log function error with context."""
    func_name = _get_func_name(func)
    logger.error(
        f"Error in {func_name}",
        exc_info=True,
        function=func_name,
        error_type=type(error).__name__,
        error_message=str(None),
        **context,
    )

x__log_function_error__mutmut_mutants : ClassVar[MutantDict] = {
'x__log_function_error__mutmut_1': x__log_function_error__mutmut_1, 
    'x__log_function_error__mutmut_2': x__log_function_error__mutmut_2, 
    'x__log_function_error__mutmut_3': x__log_function_error__mutmut_3, 
    'x__log_function_error__mutmut_4': x__log_function_error__mutmut_4, 
    'x__log_function_error__mutmut_5': x__log_function_error__mutmut_5, 
    'x__log_function_error__mutmut_6': x__log_function_error__mutmut_6, 
    'x__log_function_error__mutmut_7': x__log_function_error__mutmut_7, 
    'x__log_function_error__mutmut_8': x__log_function_error__mutmut_8, 
    'x__log_function_error__mutmut_9': x__log_function_error__mutmut_9, 
    'x__log_function_error__mutmut_10': x__log_function_error__mutmut_10, 
    'x__log_function_error__mutmut_11': x__log_function_error__mutmut_11, 
    'x__log_function_error__mutmut_12': x__log_function_error__mutmut_12, 
    'x__log_function_error__mutmut_13': x__log_function_error__mutmut_13, 
    'x__log_function_error__mutmut_14': x__log_function_error__mutmut_14, 
    'x__log_function_error__mutmut_15': x__log_function_error__mutmut_15, 
    'x__log_function_error__mutmut_16': x__log_function_error__mutmut_16
}

def _log_function_error(*args, **kwargs):
    result = _mutmut_trampoline(x__log_function_error__mutmut_orig, x__log_function_error__mutmut_mutants, args, kwargs)
    return result 

_log_function_error.__signature__ = _mutmut_signature(x__log_function_error__mutmut_orig)
x__log_function_error__mutmut_orig.__name__ = 'x__log_function_error'


def x_log_only_error_context__mutmut_orig(
    *,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    log_level: str = "debug",
    log_success: bool = False,
) -> Callable[[F], F]:
    """Safe decorator that only adds logging context without changing error behavior.

    This decorator preserves the exact original error message and type while adding
    structured logging context. It never suppresses errors or changes their behavior.

    Args:
        context_provider: Function that provides additional logging context.
        log_level: Level for operation logging ('debug', 'trace', etc.)
        log_success: Whether to log successful operations.

    Returns:
        Decorated function that preserves all original error behavior.

    Examples:
        >>> @log_only_error_context(
        ...     context_provider=lambda: {"operation": "detect_launcher_type"},
        ...     log_level="trace"
        ... )
        ... def detect_launcher_type(self, path):
        ...     # Original error messages preserved exactly
        ...     return self._internal_detect(path)

    """

    def decorator(func: F) -> F:
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                context = context_provider() if context_provider else {}
                logger = get_foundation_logger()

                _log_function_entry(logger, func, log_level, context)

                try:
                    result = await func(*args, **kwargs)

                    if log_success:
                        _log_function_success(logger, func, log_level, context)

                    return result

                except Exception as e:
                    _log_function_error(logger, func, e, context)
                    raise

            return async_wrapper  # type: ignore

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            context = context_provider() if context_provider else {}
            logger = get_foundation_logger()

            _log_function_entry(logger, func, log_level, context)

            try:
                result = func(*args, **kwargs)

                if log_success:
                    _log_function_success(logger, func, log_level, context)

                return result

            except Exception as e:
                _log_function_error(logger, func, e, context)
                raise

        return wrapper  # type: ignore

    return decorator


def x_log_only_error_context__mutmut_1(
    *,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    log_level: str = "XXdebugXX",
    log_success: bool = False,
) -> Callable[[F], F]:
    """Safe decorator that only adds logging context without changing error behavior.

    This decorator preserves the exact original error message and type while adding
    structured logging context. It never suppresses errors or changes their behavior.

    Args:
        context_provider: Function that provides additional logging context.
        log_level: Level for operation logging ('debug', 'trace', etc.)
        log_success: Whether to log successful operations.

    Returns:
        Decorated function that preserves all original error behavior.

    Examples:
        >>> @log_only_error_context(
        ...     context_provider=lambda: {"operation": "detect_launcher_type"},
        ...     log_level="trace"
        ... )
        ... def detect_launcher_type(self, path):
        ...     # Original error messages preserved exactly
        ...     return self._internal_detect(path)

    """

    def decorator(func: F) -> F:
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                context = context_provider() if context_provider else {}
                logger = get_foundation_logger()

                _log_function_entry(logger, func, log_level, context)

                try:
                    result = await func(*args, **kwargs)

                    if log_success:
                        _log_function_success(logger, func, log_level, context)

                    return result

                except Exception as e:
                    _log_function_error(logger, func, e, context)
                    raise

            return async_wrapper  # type: ignore

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            context = context_provider() if context_provider else {}
            logger = get_foundation_logger()

            _log_function_entry(logger, func, log_level, context)

            try:
                result = func(*args, **kwargs)

                if log_success:
                    _log_function_success(logger, func, log_level, context)

                return result

            except Exception as e:
                _log_function_error(logger, func, e, context)
                raise

        return wrapper  # type: ignore

    return decorator


def x_log_only_error_context__mutmut_2(
    *,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    log_level: str = "DEBUG",
    log_success: bool = False,
) -> Callable[[F], F]:
    """Safe decorator that only adds logging context without changing error behavior.

    This decorator preserves the exact original error message and type while adding
    structured logging context. It never suppresses errors or changes their behavior.

    Args:
        context_provider: Function that provides additional logging context.
        log_level: Level for operation logging ('debug', 'trace', etc.)
        log_success: Whether to log successful operations.

    Returns:
        Decorated function that preserves all original error behavior.

    Examples:
        >>> @log_only_error_context(
        ...     context_provider=lambda: {"operation": "detect_launcher_type"},
        ...     log_level="trace"
        ... )
        ... def detect_launcher_type(self, path):
        ...     # Original error messages preserved exactly
        ...     return self._internal_detect(path)

    """

    def decorator(func: F) -> F:
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                context = context_provider() if context_provider else {}
                logger = get_foundation_logger()

                _log_function_entry(logger, func, log_level, context)

                try:
                    result = await func(*args, **kwargs)

                    if log_success:
                        _log_function_success(logger, func, log_level, context)

                    return result

                except Exception as e:
                    _log_function_error(logger, func, e, context)
                    raise

            return async_wrapper  # type: ignore

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            context = context_provider() if context_provider else {}
            logger = get_foundation_logger()

            _log_function_entry(logger, func, log_level, context)

            try:
                result = func(*args, **kwargs)

                if log_success:
                    _log_function_success(logger, func, log_level, context)

                return result

            except Exception as e:
                _log_function_error(logger, func, e, context)
                raise

        return wrapper  # type: ignore

    return decorator


def x_log_only_error_context__mutmut_3(
    *,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    log_level: str = "debug",
    log_success: bool = True,
) -> Callable[[F], F]:
    """Safe decorator that only adds logging context without changing error behavior.

    This decorator preserves the exact original error message and type while adding
    structured logging context. It never suppresses errors or changes their behavior.

    Args:
        context_provider: Function that provides additional logging context.
        log_level: Level for operation logging ('debug', 'trace', etc.)
        log_success: Whether to log successful operations.

    Returns:
        Decorated function that preserves all original error behavior.

    Examples:
        >>> @log_only_error_context(
        ...     context_provider=lambda: {"operation": "detect_launcher_type"},
        ...     log_level="trace"
        ... )
        ... def detect_launcher_type(self, path):
        ...     # Original error messages preserved exactly
        ...     return self._internal_detect(path)

    """

    def decorator(func: F) -> F:
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                context = context_provider() if context_provider else {}
                logger = get_foundation_logger()

                _log_function_entry(logger, func, log_level, context)

                try:
                    result = await func(*args, **kwargs)

                    if log_success:
                        _log_function_success(logger, func, log_level, context)

                    return result

                except Exception as e:
                    _log_function_error(logger, func, e, context)
                    raise

            return async_wrapper  # type: ignore

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            context = context_provider() if context_provider else {}
            logger = get_foundation_logger()

            _log_function_entry(logger, func, log_level, context)

            try:
                result = func(*args, **kwargs)

                if log_success:
                    _log_function_success(logger, func, log_level, context)

                return result

            except Exception as e:
                _log_function_error(logger, func, e, context)
                raise

        return wrapper  # type: ignore

    return decorator


def x_log_only_error_context__mutmut_4(
    *,
    context_provider: Callable[[], dict[str, Any]] | None = None,
    log_level: str = "debug",
    log_success: bool = False,
) -> Callable[[F], F]:
    """Safe decorator that only adds logging context without changing error behavior.

    This decorator preserves the exact original error message and type while adding
    structured logging context. It never suppresses errors or changes their behavior.

    Args:
        context_provider: Function that provides additional logging context.
        log_level: Level for operation logging ('debug', 'trace', etc.)
        log_success: Whether to log successful operations.

    Returns:
        Decorated function that preserves all original error behavior.

    Examples:
        >>> @log_only_error_context(
        ...     context_provider=lambda: {"operation": "detect_launcher_type"},
        ...     log_level="trace"
        ... )
        ... def detect_launcher_type(self, path):
        ...     # Original error messages preserved exactly
        ...     return self._internal_detect(path)

    """

    def decorator(func: F) -> F:
        if inspect.iscoroutinefunction(None):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                context = context_provider() if context_provider else {}
                logger = get_foundation_logger()

                _log_function_entry(logger, func, log_level, context)

                try:
                    result = await func(*args, **kwargs)

                    if log_success:
                        _log_function_success(logger, func, log_level, context)

                    return result

                except Exception as e:
                    _log_function_error(logger, func, e, context)
                    raise

            return async_wrapper  # type: ignore

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            context = context_provider() if context_provider else {}
            logger = get_foundation_logger()

            _log_function_entry(logger, func, log_level, context)

            try:
                result = func(*args, **kwargs)

                if log_success:
                    _log_function_success(logger, func, log_level, context)

                return result

            except Exception as e:
                _log_function_error(logger, func, e, context)
                raise

        return wrapper  # type: ignore

    return decorator

x_log_only_error_context__mutmut_mutants : ClassVar[MutantDict] = {
'x_log_only_error_context__mutmut_1': x_log_only_error_context__mutmut_1, 
    'x_log_only_error_context__mutmut_2': x_log_only_error_context__mutmut_2, 
    'x_log_only_error_context__mutmut_3': x_log_only_error_context__mutmut_3, 
    'x_log_only_error_context__mutmut_4': x_log_only_error_context__mutmut_4
}

def log_only_error_context(*args, **kwargs):
    result = _mutmut_trampoline(x_log_only_error_context__mutmut_orig, x_log_only_error_context__mutmut_mutants, args, kwargs)
    return result 

log_only_error_context.__signature__ = _mutmut_signature(x_log_only_error_context__mutmut_orig)
x_log_only_error_context__mutmut_orig.__name__ = 'x_log_only_error_context'


# <3 🧱🤝🐛🪄
