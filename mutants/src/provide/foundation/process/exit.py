# provide/foundation/process/exit.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import sys

from provide.foundation.config.defaults import EXIT_ERROR, EXIT_SIGINT, EXIT_SUCCESS
from provide.foundation.hub.foundation import get_foundation_logger

"""Process exit utilities for standardized exit handling."""
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


def x_exit_success__mutmut_orig(message: str | None = None) -> None:
    """Exit with success status.

    Args:
        message: Optional message to log before exiting

    """
    if message:
        logger = get_foundation_logger()
        logger.info(f"Exiting successfully: {message}")
    sys.exit(EXIT_SUCCESS)


def x_exit_success__mutmut_1(message: str | None = None) -> None:
    """Exit with success status.

    Args:
        message: Optional message to log before exiting

    """
    if message:
        logger = None
        logger.info(f"Exiting successfully: {message}")
    sys.exit(EXIT_SUCCESS)


def x_exit_success__mutmut_2(message: str | None = None) -> None:
    """Exit with success status.

    Args:
        message: Optional message to log before exiting

    """
    if message:
        logger = get_foundation_logger()
        logger.info(None)
    sys.exit(EXIT_SUCCESS)


def x_exit_success__mutmut_3(message: str | None = None) -> None:
    """Exit with success status.

    Args:
        message: Optional message to log before exiting

    """
    if message:
        logger = get_foundation_logger()
        logger.info(f"Exiting successfully: {message}")
    sys.exit(None)

x_exit_success__mutmut_mutants : ClassVar[MutantDict] = {
'x_exit_success__mutmut_1': x_exit_success__mutmut_1, 
    'x_exit_success__mutmut_2': x_exit_success__mutmut_2, 
    'x_exit_success__mutmut_3': x_exit_success__mutmut_3
}

def exit_success(*args, **kwargs):
    result = _mutmut_trampoline(x_exit_success__mutmut_orig, x_exit_success__mutmut_mutants, args, kwargs)
    return result 

exit_success.__signature__ = _mutmut_signature(x_exit_success__mutmut_orig)
x_exit_success__mutmut_orig.__name__ = 'x_exit_success'


def x_exit_error__mutmut_orig(message: str | None = None, code: int = EXIT_ERROR) -> None:
    """Exit with error status.

    Args:
        message: Optional error message to log before exiting
        code: Exit code to use (defaults to EXIT_ERROR)

    """
    if message:
        logger = get_foundation_logger()
        logger.error(f"Exiting with error: {message}", exit_code=code)
    sys.exit(code)


def x_exit_error__mutmut_1(message: str | None = None, code: int = EXIT_ERROR) -> None:
    """Exit with error status.

    Args:
        message: Optional error message to log before exiting
        code: Exit code to use (defaults to EXIT_ERROR)

    """
    if message:
        logger = None
        logger.error(f"Exiting with error: {message}", exit_code=code)
    sys.exit(code)


def x_exit_error__mutmut_2(message: str | None = None, code: int = EXIT_ERROR) -> None:
    """Exit with error status.

    Args:
        message: Optional error message to log before exiting
        code: Exit code to use (defaults to EXIT_ERROR)

    """
    if message:
        logger = get_foundation_logger()
        logger.error(None, exit_code=code)
    sys.exit(code)


def x_exit_error__mutmut_3(message: str | None = None, code: int = EXIT_ERROR) -> None:
    """Exit with error status.

    Args:
        message: Optional error message to log before exiting
        code: Exit code to use (defaults to EXIT_ERROR)

    """
    if message:
        logger = get_foundation_logger()
        logger.error(f"Exiting with error: {message}", exit_code=None)
    sys.exit(code)


def x_exit_error__mutmut_4(message: str | None = None, code: int = EXIT_ERROR) -> None:
    """Exit with error status.

    Args:
        message: Optional error message to log before exiting
        code: Exit code to use (defaults to EXIT_ERROR)

    """
    if message:
        logger = get_foundation_logger()
        logger.error(exit_code=code)
    sys.exit(code)


def x_exit_error__mutmut_5(message: str | None = None, code: int = EXIT_ERROR) -> None:
    """Exit with error status.

    Args:
        message: Optional error message to log before exiting
        code: Exit code to use (defaults to EXIT_ERROR)

    """
    if message:
        logger = get_foundation_logger()
        logger.error(f"Exiting with error: {message}", )
    sys.exit(code)


def x_exit_error__mutmut_6(message: str | None = None, code: int = EXIT_ERROR) -> None:
    """Exit with error status.

    Args:
        message: Optional error message to log before exiting
        code: Exit code to use (defaults to EXIT_ERROR)

    """
    if message:
        logger = get_foundation_logger()
        logger.error(f"Exiting with error: {message}", exit_code=code)
    sys.exit(None)

x_exit_error__mutmut_mutants : ClassVar[MutantDict] = {
'x_exit_error__mutmut_1': x_exit_error__mutmut_1, 
    'x_exit_error__mutmut_2': x_exit_error__mutmut_2, 
    'x_exit_error__mutmut_3': x_exit_error__mutmut_3, 
    'x_exit_error__mutmut_4': x_exit_error__mutmut_4, 
    'x_exit_error__mutmut_5': x_exit_error__mutmut_5, 
    'x_exit_error__mutmut_6': x_exit_error__mutmut_6
}

def exit_error(*args, **kwargs):
    result = _mutmut_trampoline(x_exit_error__mutmut_orig, x_exit_error__mutmut_mutants, args, kwargs)
    return result 

exit_error.__signature__ = _mutmut_signature(x_exit_error__mutmut_orig)
x_exit_error__mutmut_orig.__name__ = 'x_exit_error'


def x_exit_interrupted__mutmut_orig(message: str = "Process interrupted") -> None:
    """Exit due to interrupt signal (SIGINT).

    Args:
        message: Message to log before exiting

    """
    logger = get_foundation_logger()
    logger.warning(f"Exiting due to interrupt: {message}")
    sys.exit(EXIT_SIGINT)


def x_exit_interrupted__mutmut_1(message: str = "XXProcess interruptedXX") -> None:
    """Exit due to interrupt signal (SIGINT).

    Args:
        message: Message to log before exiting

    """
    logger = get_foundation_logger()
    logger.warning(f"Exiting due to interrupt: {message}")
    sys.exit(EXIT_SIGINT)


def x_exit_interrupted__mutmut_2(message: str = "process interrupted") -> None:
    """Exit due to interrupt signal (SIGINT).

    Args:
        message: Message to log before exiting

    """
    logger = get_foundation_logger()
    logger.warning(f"Exiting due to interrupt: {message}")
    sys.exit(EXIT_SIGINT)


def x_exit_interrupted__mutmut_3(message: str = "PROCESS INTERRUPTED") -> None:
    """Exit due to interrupt signal (SIGINT).

    Args:
        message: Message to log before exiting

    """
    logger = get_foundation_logger()
    logger.warning(f"Exiting due to interrupt: {message}")
    sys.exit(EXIT_SIGINT)


def x_exit_interrupted__mutmut_4(message: str = "Process interrupted") -> None:
    """Exit due to interrupt signal (SIGINT).

    Args:
        message: Message to log before exiting

    """
    logger = None
    logger.warning(f"Exiting due to interrupt: {message}")
    sys.exit(EXIT_SIGINT)


def x_exit_interrupted__mutmut_5(message: str = "Process interrupted") -> None:
    """Exit due to interrupt signal (SIGINT).

    Args:
        message: Message to log before exiting

    """
    logger = get_foundation_logger()
    logger.warning(None)
    sys.exit(EXIT_SIGINT)


def x_exit_interrupted__mutmut_6(message: str = "Process interrupted") -> None:
    """Exit due to interrupt signal (SIGINT).

    Args:
        message: Message to log before exiting

    """
    logger = get_foundation_logger()
    logger.warning(f"Exiting due to interrupt: {message}")
    sys.exit(None)

x_exit_interrupted__mutmut_mutants : ClassVar[MutantDict] = {
'x_exit_interrupted__mutmut_1': x_exit_interrupted__mutmut_1, 
    'x_exit_interrupted__mutmut_2': x_exit_interrupted__mutmut_2, 
    'x_exit_interrupted__mutmut_3': x_exit_interrupted__mutmut_3, 
    'x_exit_interrupted__mutmut_4': x_exit_interrupted__mutmut_4, 
    'x_exit_interrupted__mutmut_5': x_exit_interrupted__mutmut_5, 
    'x_exit_interrupted__mutmut_6': x_exit_interrupted__mutmut_6
}

def exit_interrupted(*args, **kwargs):
    result = _mutmut_trampoline(x_exit_interrupted__mutmut_orig, x_exit_interrupted__mutmut_mutants, args, kwargs)
    return result 

exit_interrupted.__signature__ = _mutmut_signature(x_exit_interrupted__mutmut_orig)
x_exit_interrupted__mutmut_orig.__name__ = 'x_exit_interrupted'


# <3 🧱🤝🏃🪄
