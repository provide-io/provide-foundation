# provide/foundation/cli/utils.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Common CLI utilities for output, logging, and testing."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from click.testing import CliRunner, Result

from provide.foundation import get_hub
from provide.foundation.console.output import perr, pout
from provide.foundation.context import CLIContext
from provide.foundation.logger import (
    LoggingConfig,
    TelemetryConfig,
    get_logger,
)

if TYPE_CHECKING:
    import click as click_types

log = get_logger(__name__)
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


def x_echo_json__mutmut_orig(data: Any, err: bool = False) -> None:
    """Output data as JSON.

    Args:
        data: Data to output as JSON
        err: Whether to output to stderr

    """
    if err:
        perr(data)
    else:
        pout(data)


def x_echo_json__mutmut_1(data: Any, err: bool = True) -> None:
    """Output data as JSON.

    Args:
        data: Data to output as JSON
        err: Whether to output to stderr

    """
    if err:
        perr(data)
    else:
        pout(data)


def x_echo_json__mutmut_2(data: Any, err: bool = False) -> None:
    """Output data as JSON.

    Args:
        data: Data to output as JSON
        err: Whether to output to stderr

    """
    if err:
        perr(None)
    else:
        pout(data)


def x_echo_json__mutmut_3(data: Any, err: bool = False) -> None:
    """Output data as JSON.

    Args:
        data: Data to output as JSON
        err: Whether to output to stderr

    """
    if err:
        perr(data)
    else:
        pout(None)

x_echo_json__mutmut_mutants : ClassVar[MutantDict] = {
'x_echo_json__mutmut_1': x_echo_json__mutmut_1, 
    'x_echo_json__mutmut_2': x_echo_json__mutmut_2, 
    'x_echo_json__mutmut_3': x_echo_json__mutmut_3
}

def echo_json(*args, **kwargs):
    result = _mutmut_trampoline(x_echo_json__mutmut_orig, x_echo_json__mutmut_mutants, args, kwargs)
    return result 

echo_json.__signature__ = _mutmut_signature(x_echo_json__mutmut_orig)
x_echo_json__mutmut_orig.__name__ = 'x_echo_json'


def x_echo_error__mutmut_orig(message: str, json_output: bool = False) -> None:
    """Output an error message.

    Args:
        message: Error message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(message, json_key="error")
    else:
        perr(f"✗ {message}", color="red")


def x_echo_error__mutmut_1(message: str, json_output: bool = True) -> None:
    """Output an error message.

    Args:
        message: Error message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(message, json_key="error")
    else:
        perr(f"✗ {message}", color="red")


def x_echo_error__mutmut_2(message: str, json_output: bool = False) -> None:
    """Output an error message.

    Args:
        message: Error message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(None, json_key="error")
    else:
        perr(f"✗ {message}", color="red")


def x_echo_error__mutmut_3(message: str, json_output: bool = False) -> None:
    """Output an error message.

    Args:
        message: Error message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(message, json_key=None)
    else:
        perr(f"✗ {message}", color="red")


def x_echo_error__mutmut_4(message: str, json_output: bool = False) -> None:
    """Output an error message.

    Args:
        message: Error message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(json_key="error")
    else:
        perr(f"✗ {message}", color="red")


def x_echo_error__mutmut_5(message: str, json_output: bool = False) -> None:
    """Output an error message.

    Args:
        message: Error message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(message, )
    else:
        perr(f"✗ {message}", color="red")


def x_echo_error__mutmut_6(message: str, json_output: bool = False) -> None:
    """Output an error message.

    Args:
        message: Error message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(message, json_key="XXerrorXX")
    else:
        perr(f"✗ {message}", color="red")


def x_echo_error__mutmut_7(message: str, json_output: bool = False) -> None:
    """Output an error message.

    Args:
        message: Error message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(message, json_key="ERROR")
    else:
        perr(f"✗ {message}", color="red")


def x_echo_error__mutmut_8(message: str, json_output: bool = False) -> None:
    """Output an error message.

    Args:
        message: Error message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(message, json_key="error")
    else:
        perr(None, color="red")


def x_echo_error__mutmut_9(message: str, json_output: bool = False) -> None:
    """Output an error message.

    Args:
        message: Error message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(message, json_key="error")
    else:
        perr(f"✗ {message}", color=None)


def x_echo_error__mutmut_10(message: str, json_output: bool = False) -> None:
    """Output an error message.

    Args:
        message: Error message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(message, json_key="error")
    else:
        perr(color="red")


def x_echo_error__mutmut_11(message: str, json_output: bool = False) -> None:
    """Output an error message.

    Args:
        message: Error message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(message, json_key="error")
    else:
        perr(f"✗ {message}", )


def x_echo_error__mutmut_12(message: str, json_output: bool = False) -> None:
    """Output an error message.

    Args:
        message: Error message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(message, json_key="error")
    else:
        perr(f"✗ {message}", color="XXredXX")


def x_echo_error__mutmut_13(message: str, json_output: bool = False) -> None:
    """Output an error message.

    Args:
        message: Error message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(message, json_key="error")
    else:
        perr(f"✗ {message}", color="RED")

x_echo_error__mutmut_mutants : ClassVar[MutantDict] = {
'x_echo_error__mutmut_1': x_echo_error__mutmut_1, 
    'x_echo_error__mutmut_2': x_echo_error__mutmut_2, 
    'x_echo_error__mutmut_3': x_echo_error__mutmut_3, 
    'x_echo_error__mutmut_4': x_echo_error__mutmut_4, 
    'x_echo_error__mutmut_5': x_echo_error__mutmut_5, 
    'x_echo_error__mutmut_6': x_echo_error__mutmut_6, 
    'x_echo_error__mutmut_7': x_echo_error__mutmut_7, 
    'x_echo_error__mutmut_8': x_echo_error__mutmut_8, 
    'x_echo_error__mutmut_9': x_echo_error__mutmut_9, 
    'x_echo_error__mutmut_10': x_echo_error__mutmut_10, 
    'x_echo_error__mutmut_11': x_echo_error__mutmut_11, 
    'x_echo_error__mutmut_12': x_echo_error__mutmut_12, 
    'x_echo_error__mutmut_13': x_echo_error__mutmut_13
}

def echo_error(*args, **kwargs):
    result = _mutmut_trampoline(x_echo_error__mutmut_orig, x_echo_error__mutmut_mutants, args, kwargs)
    return result 

echo_error.__signature__ = _mutmut_signature(x_echo_error__mutmut_orig)
x_echo_error__mutmut_orig.__name__ = 'x_echo_error'


def x_echo_success__mutmut_orig(message: str, json_output: bool = False) -> None:
    """Output a success message.

    Args:
        message: Success message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        pout(message, json_key="success")
    else:
        pout(f"✓ {message}", color="green")


def x_echo_success__mutmut_1(message: str, json_output: bool = True) -> None:
    """Output a success message.

    Args:
        message: Success message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        pout(message, json_key="success")
    else:
        pout(f"✓ {message}", color="green")


def x_echo_success__mutmut_2(message: str, json_output: bool = False) -> None:
    """Output a success message.

    Args:
        message: Success message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        pout(None, json_key="success")
    else:
        pout(f"✓ {message}", color="green")


def x_echo_success__mutmut_3(message: str, json_output: bool = False) -> None:
    """Output a success message.

    Args:
        message: Success message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        pout(message, json_key=None)
    else:
        pout(f"✓ {message}", color="green")


def x_echo_success__mutmut_4(message: str, json_output: bool = False) -> None:
    """Output a success message.

    Args:
        message: Success message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        pout(json_key="success")
    else:
        pout(f"✓ {message}", color="green")


def x_echo_success__mutmut_5(message: str, json_output: bool = False) -> None:
    """Output a success message.

    Args:
        message: Success message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        pout(message, )
    else:
        pout(f"✓ {message}", color="green")


def x_echo_success__mutmut_6(message: str, json_output: bool = False) -> None:
    """Output a success message.

    Args:
        message: Success message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        pout(message, json_key="XXsuccessXX")
    else:
        pout(f"✓ {message}", color="green")


def x_echo_success__mutmut_7(message: str, json_output: bool = False) -> None:
    """Output a success message.

    Args:
        message: Success message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        pout(message, json_key="SUCCESS")
    else:
        pout(f"✓ {message}", color="green")


def x_echo_success__mutmut_8(message: str, json_output: bool = False) -> None:
    """Output a success message.

    Args:
        message: Success message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        pout(message, json_key="success")
    else:
        pout(None, color="green")


def x_echo_success__mutmut_9(message: str, json_output: bool = False) -> None:
    """Output a success message.

    Args:
        message: Success message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        pout(message, json_key="success")
    else:
        pout(f"✓ {message}", color=None)


def x_echo_success__mutmut_10(message: str, json_output: bool = False) -> None:
    """Output a success message.

    Args:
        message: Success message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        pout(message, json_key="success")
    else:
        pout(color="green")


def x_echo_success__mutmut_11(message: str, json_output: bool = False) -> None:
    """Output a success message.

    Args:
        message: Success message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        pout(message, json_key="success")
    else:
        pout(f"✓ {message}", )


def x_echo_success__mutmut_12(message: str, json_output: bool = False) -> None:
    """Output a success message.

    Args:
        message: Success message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        pout(message, json_key="success")
    else:
        pout(f"✓ {message}", color="XXgreenXX")


def x_echo_success__mutmut_13(message: str, json_output: bool = False) -> None:
    """Output a success message.

    Args:
        message: Success message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        pout(message, json_key="success")
    else:
        pout(f"✓ {message}", color="GREEN")

x_echo_success__mutmut_mutants : ClassVar[MutantDict] = {
'x_echo_success__mutmut_1': x_echo_success__mutmut_1, 
    'x_echo_success__mutmut_2': x_echo_success__mutmut_2, 
    'x_echo_success__mutmut_3': x_echo_success__mutmut_3, 
    'x_echo_success__mutmut_4': x_echo_success__mutmut_4, 
    'x_echo_success__mutmut_5': x_echo_success__mutmut_5, 
    'x_echo_success__mutmut_6': x_echo_success__mutmut_6, 
    'x_echo_success__mutmut_7': x_echo_success__mutmut_7, 
    'x_echo_success__mutmut_8': x_echo_success__mutmut_8, 
    'x_echo_success__mutmut_9': x_echo_success__mutmut_9, 
    'x_echo_success__mutmut_10': x_echo_success__mutmut_10, 
    'x_echo_success__mutmut_11': x_echo_success__mutmut_11, 
    'x_echo_success__mutmut_12': x_echo_success__mutmut_12, 
    'x_echo_success__mutmut_13': x_echo_success__mutmut_13
}

def echo_success(*args, **kwargs):
    result = _mutmut_trampoline(x_echo_success__mutmut_orig, x_echo_success__mutmut_mutants, args, kwargs)
    return result 

echo_success.__signature__ = _mutmut_signature(x_echo_success__mutmut_orig)
x_echo_success__mutmut_orig.__name__ = 'x_echo_success'


def x_echo_warning__mutmut_orig(message: str, json_output: bool = False) -> None:
    """Output a warning message.

    Args:
        message: Warning message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(message, json_key="warning")
    else:
        perr(f"⚠ {message}", color="yellow")


def x_echo_warning__mutmut_1(message: str, json_output: bool = True) -> None:
    """Output a warning message.

    Args:
        message: Warning message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(message, json_key="warning")
    else:
        perr(f"⚠ {message}", color="yellow")


def x_echo_warning__mutmut_2(message: str, json_output: bool = False) -> None:
    """Output a warning message.

    Args:
        message: Warning message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(None, json_key="warning")
    else:
        perr(f"⚠ {message}", color="yellow")


def x_echo_warning__mutmut_3(message: str, json_output: bool = False) -> None:
    """Output a warning message.

    Args:
        message: Warning message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(message, json_key=None)
    else:
        perr(f"⚠ {message}", color="yellow")


def x_echo_warning__mutmut_4(message: str, json_output: bool = False) -> None:
    """Output a warning message.

    Args:
        message: Warning message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(json_key="warning")
    else:
        perr(f"⚠ {message}", color="yellow")


def x_echo_warning__mutmut_5(message: str, json_output: bool = False) -> None:
    """Output a warning message.

    Args:
        message: Warning message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(message, )
    else:
        perr(f"⚠ {message}", color="yellow")


def x_echo_warning__mutmut_6(message: str, json_output: bool = False) -> None:
    """Output a warning message.

    Args:
        message: Warning message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(message, json_key="XXwarningXX")
    else:
        perr(f"⚠ {message}", color="yellow")


def x_echo_warning__mutmut_7(message: str, json_output: bool = False) -> None:
    """Output a warning message.

    Args:
        message: Warning message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(message, json_key="WARNING")
    else:
        perr(f"⚠ {message}", color="yellow")


def x_echo_warning__mutmut_8(message: str, json_output: bool = False) -> None:
    """Output a warning message.

    Args:
        message: Warning message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(message, json_key="warning")
    else:
        perr(None, color="yellow")


def x_echo_warning__mutmut_9(message: str, json_output: bool = False) -> None:
    """Output a warning message.

    Args:
        message: Warning message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(message, json_key="warning")
    else:
        perr(f"⚠ {message}", color=None)


def x_echo_warning__mutmut_10(message: str, json_output: bool = False) -> None:
    """Output a warning message.

    Args:
        message: Warning message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(message, json_key="warning")
    else:
        perr(color="yellow")


def x_echo_warning__mutmut_11(message: str, json_output: bool = False) -> None:
    """Output a warning message.

    Args:
        message: Warning message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(message, json_key="warning")
    else:
        perr(f"⚠ {message}", )


def x_echo_warning__mutmut_12(message: str, json_output: bool = False) -> None:
    """Output a warning message.

    Args:
        message: Warning message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(message, json_key="warning")
    else:
        perr(f"⚠ {message}", color="XXyellowXX")


def x_echo_warning__mutmut_13(message: str, json_output: bool = False) -> None:
    """Output a warning message.

    Args:
        message: Warning message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        perr(message, json_key="warning")
    else:
        perr(f"⚠ {message}", color="YELLOW")

x_echo_warning__mutmut_mutants : ClassVar[MutantDict] = {
'x_echo_warning__mutmut_1': x_echo_warning__mutmut_1, 
    'x_echo_warning__mutmut_2': x_echo_warning__mutmut_2, 
    'x_echo_warning__mutmut_3': x_echo_warning__mutmut_3, 
    'x_echo_warning__mutmut_4': x_echo_warning__mutmut_4, 
    'x_echo_warning__mutmut_5': x_echo_warning__mutmut_5, 
    'x_echo_warning__mutmut_6': x_echo_warning__mutmut_6, 
    'x_echo_warning__mutmut_7': x_echo_warning__mutmut_7, 
    'x_echo_warning__mutmut_8': x_echo_warning__mutmut_8, 
    'x_echo_warning__mutmut_9': x_echo_warning__mutmut_9, 
    'x_echo_warning__mutmut_10': x_echo_warning__mutmut_10, 
    'x_echo_warning__mutmut_11': x_echo_warning__mutmut_11, 
    'x_echo_warning__mutmut_12': x_echo_warning__mutmut_12, 
    'x_echo_warning__mutmut_13': x_echo_warning__mutmut_13
}

def echo_warning(*args, **kwargs):
    result = _mutmut_trampoline(x_echo_warning__mutmut_orig, x_echo_warning__mutmut_mutants, args, kwargs)
    return result 

echo_warning.__signature__ = _mutmut_signature(x_echo_warning__mutmut_orig)
x_echo_warning__mutmut_orig.__name__ = 'x_echo_warning'


def x_echo_info__mutmut_orig(message: str, json_output: bool = False) -> None:
    """Output an informational message.

    Args:
        message: Info message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        pout(message, json_key="info")
    else:
        pout(f"i {message}")


def x_echo_info__mutmut_1(message: str, json_output: bool = True) -> None:
    """Output an informational message.

    Args:
        message: Info message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        pout(message, json_key="info")
    else:
        pout(f"i {message}")


def x_echo_info__mutmut_2(message: str, json_output: bool = False) -> None:
    """Output an informational message.

    Args:
        message: Info message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        pout(None, json_key="info")
    else:
        pout(f"i {message}")


def x_echo_info__mutmut_3(message: str, json_output: bool = False) -> None:
    """Output an informational message.

    Args:
        message: Info message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        pout(message, json_key=None)
    else:
        pout(f"i {message}")


def x_echo_info__mutmut_4(message: str, json_output: bool = False) -> None:
    """Output an informational message.

    Args:
        message: Info message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        pout(json_key="info")
    else:
        pout(f"i {message}")


def x_echo_info__mutmut_5(message: str, json_output: bool = False) -> None:
    """Output an informational message.

    Args:
        message: Info message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        pout(message, )
    else:
        pout(f"i {message}")


def x_echo_info__mutmut_6(message: str, json_output: bool = False) -> None:
    """Output an informational message.

    Args:
        message: Info message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        pout(message, json_key="XXinfoXX")
    else:
        pout(f"i {message}")


def x_echo_info__mutmut_7(message: str, json_output: bool = False) -> None:
    """Output an informational message.

    Args:
        message: Info message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        pout(message, json_key="INFO")
    else:
        pout(f"i {message}")


def x_echo_info__mutmut_8(message: str, json_output: bool = False) -> None:
    """Output an informational message.

    Args:
        message: Info message to output
        json_output: Whether to output as JSON

    """
    if json_output:
        pout(message, json_key="info")
    else:
        pout(None)

x_echo_info__mutmut_mutants : ClassVar[MutantDict] = {
'x_echo_info__mutmut_1': x_echo_info__mutmut_1, 
    'x_echo_info__mutmut_2': x_echo_info__mutmut_2, 
    'x_echo_info__mutmut_3': x_echo_info__mutmut_3, 
    'x_echo_info__mutmut_4': x_echo_info__mutmut_4, 
    'x_echo_info__mutmut_5': x_echo_info__mutmut_5, 
    'x_echo_info__mutmut_6': x_echo_info__mutmut_6, 
    'x_echo_info__mutmut_7': x_echo_info__mutmut_7, 
    'x_echo_info__mutmut_8': x_echo_info__mutmut_8
}

def echo_info(*args, **kwargs):
    result = _mutmut_trampoline(x_echo_info__mutmut_orig, x_echo_info__mutmut_mutants, args, kwargs)
    return result 

echo_info.__signature__ = _mutmut_signature(x_echo_info__mutmut_orig)
x_echo_info__mutmut_orig.__name__ = 'x_echo_info'


def x_setup_cli_logging__mutmut_orig(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_1(
    ctx: CLIContext,
    reinit_logging: bool = False,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_2(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = None

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_3(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "XXjsonXX" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_4(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "JSON" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_5(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = None

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_6(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=None,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_7(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=None,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_8(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=None,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_9(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=None,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_10(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=None,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_11(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=None,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_12(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_13(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_14(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_15(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=False,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_16(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_17(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_18(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=True,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_19(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_20(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_21(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = None

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_22(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=None,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_23(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=None,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_24(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_25(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_26(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = None
    hub.initialize_foundation(config=telemetry_config, force=reinit_logging)


def x_setup_cli_logging__mutmut_27(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=None, force=reinit_logging)


def x_setup_cli_logging__mutmut_28(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, force=None)


def x_setup_cli_logging__mutmut_29(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(force=reinit_logging)


def x_setup_cli_logging__mutmut_30(
    ctx: CLIContext,
    reinit_logging: bool = True,
) -> None:
    """Setup logging for CLI applications using a CLIContext object.

    This function is the designated way to configure logging within a CLI
    application built with foundation. It uses the provided context object
    to construct a full TelemetryConfig and initializes the system.

    Args:
        ctx: The foundation CLIContext, populated by CLI decorators.
        reinit_logging: Whether to force re-initialization of logging (default: True).
            Set to False when embedding Foundation in a host application to avoid
            clobbering the host's logging configuration.

    """
    console_formatter = "json" if ctx.json_output else ctx.log_format

    logging_config = LoggingConfig(
        default_level=ctx.log_level,  # type: ignore[arg-type]
        console_formatter=console_formatter,  # type: ignore[arg-type]
        omit_timestamp=False,
        logger_name_emoji_prefix_enabled=not ctx.no_emoji,
        das_emoji_prefix_enabled=not ctx.no_emoji,
        log_file=ctx.log_file,
    )

    telemetry_config = TelemetryConfig(
        service_name=ctx.profile,
        logging=logging_config,
    )

    hub = get_hub()
    hub.initialize_foundation(config=telemetry_config, )

x_setup_cli_logging__mutmut_mutants : ClassVar[MutantDict] = {
'x_setup_cli_logging__mutmut_1': x_setup_cli_logging__mutmut_1, 
    'x_setup_cli_logging__mutmut_2': x_setup_cli_logging__mutmut_2, 
    'x_setup_cli_logging__mutmut_3': x_setup_cli_logging__mutmut_3, 
    'x_setup_cli_logging__mutmut_4': x_setup_cli_logging__mutmut_4, 
    'x_setup_cli_logging__mutmut_5': x_setup_cli_logging__mutmut_5, 
    'x_setup_cli_logging__mutmut_6': x_setup_cli_logging__mutmut_6, 
    'x_setup_cli_logging__mutmut_7': x_setup_cli_logging__mutmut_7, 
    'x_setup_cli_logging__mutmut_8': x_setup_cli_logging__mutmut_8, 
    'x_setup_cli_logging__mutmut_9': x_setup_cli_logging__mutmut_9, 
    'x_setup_cli_logging__mutmut_10': x_setup_cli_logging__mutmut_10, 
    'x_setup_cli_logging__mutmut_11': x_setup_cli_logging__mutmut_11, 
    'x_setup_cli_logging__mutmut_12': x_setup_cli_logging__mutmut_12, 
    'x_setup_cli_logging__mutmut_13': x_setup_cli_logging__mutmut_13, 
    'x_setup_cli_logging__mutmut_14': x_setup_cli_logging__mutmut_14, 
    'x_setup_cli_logging__mutmut_15': x_setup_cli_logging__mutmut_15, 
    'x_setup_cli_logging__mutmut_16': x_setup_cli_logging__mutmut_16, 
    'x_setup_cli_logging__mutmut_17': x_setup_cli_logging__mutmut_17, 
    'x_setup_cli_logging__mutmut_18': x_setup_cli_logging__mutmut_18, 
    'x_setup_cli_logging__mutmut_19': x_setup_cli_logging__mutmut_19, 
    'x_setup_cli_logging__mutmut_20': x_setup_cli_logging__mutmut_20, 
    'x_setup_cli_logging__mutmut_21': x_setup_cli_logging__mutmut_21, 
    'x_setup_cli_logging__mutmut_22': x_setup_cli_logging__mutmut_22, 
    'x_setup_cli_logging__mutmut_23': x_setup_cli_logging__mutmut_23, 
    'x_setup_cli_logging__mutmut_24': x_setup_cli_logging__mutmut_24, 
    'x_setup_cli_logging__mutmut_25': x_setup_cli_logging__mutmut_25, 
    'x_setup_cli_logging__mutmut_26': x_setup_cli_logging__mutmut_26, 
    'x_setup_cli_logging__mutmut_27': x_setup_cli_logging__mutmut_27, 
    'x_setup_cli_logging__mutmut_28': x_setup_cli_logging__mutmut_28, 
    'x_setup_cli_logging__mutmut_29': x_setup_cli_logging__mutmut_29, 
    'x_setup_cli_logging__mutmut_30': x_setup_cli_logging__mutmut_30
}

def setup_cli_logging(*args, **kwargs):
    result = _mutmut_trampoline(x_setup_cli_logging__mutmut_orig, x_setup_cli_logging__mutmut_mutants, args, kwargs)
    return result 

setup_cli_logging.__signature__ = _mutmut_signature(x_setup_cli_logging__mutmut_orig)
x_setup_cli_logging__mutmut_orig.__name__ = 'x_setup_cli_logging'


def x_create_cli_context__mutmut_orig(**kwargs: Any) -> CLIContext:
    """Create a CLIContext for CLI usage.

    Loads from environment, then overlays any provided kwargs.

    Args:
        **kwargs: Override values for the context

    Returns:
        Configured CLIContext instance

    """
    ctx = CLIContext.from_env()
    for key, value in kwargs.items():
        if value is not None and hasattr(ctx, key):
            setattr(ctx, key, value)
    return ctx


def x_create_cli_context__mutmut_1(**kwargs: Any) -> CLIContext:
    """Create a CLIContext for CLI usage.

    Loads from environment, then overlays any provided kwargs.

    Args:
        **kwargs: Override values for the context

    Returns:
        Configured CLIContext instance

    """
    ctx = None
    for key, value in kwargs.items():
        if value is not None and hasattr(ctx, key):
            setattr(ctx, key, value)
    return ctx


def x_create_cli_context__mutmut_2(**kwargs: Any) -> CLIContext:
    """Create a CLIContext for CLI usage.

    Loads from environment, then overlays any provided kwargs.

    Args:
        **kwargs: Override values for the context

    Returns:
        Configured CLIContext instance

    """
    ctx = CLIContext.from_env()
    for key, value in kwargs.items():
        if value is not None or hasattr(ctx, key):
            setattr(ctx, key, value)
    return ctx


def x_create_cli_context__mutmut_3(**kwargs: Any) -> CLIContext:
    """Create a CLIContext for CLI usage.

    Loads from environment, then overlays any provided kwargs.

    Args:
        **kwargs: Override values for the context

    Returns:
        Configured CLIContext instance

    """
    ctx = CLIContext.from_env()
    for key, value in kwargs.items():
        if value is None and hasattr(ctx, key):
            setattr(ctx, key, value)
    return ctx


def x_create_cli_context__mutmut_4(**kwargs: Any) -> CLIContext:
    """Create a CLIContext for CLI usage.

    Loads from environment, then overlays any provided kwargs.

    Args:
        **kwargs: Override values for the context

    Returns:
        Configured CLIContext instance

    """
    ctx = CLIContext.from_env()
    for key, value in kwargs.items():
        if value is not None and hasattr(None, key):
            setattr(ctx, key, value)
    return ctx


def x_create_cli_context__mutmut_5(**kwargs: Any) -> CLIContext:
    """Create a CLIContext for CLI usage.

    Loads from environment, then overlays any provided kwargs.

    Args:
        **kwargs: Override values for the context

    Returns:
        Configured CLIContext instance

    """
    ctx = CLIContext.from_env()
    for key, value in kwargs.items():
        if value is not None and hasattr(ctx, None):
            setattr(ctx, key, value)
    return ctx


def x_create_cli_context__mutmut_6(**kwargs: Any) -> CLIContext:
    """Create a CLIContext for CLI usage.

    Loads from environment, then overlays any provided kwargs.

    Args:
        **kwargs: Override values for the context

    Returns:
        Configured CLIContext instance

    """
    ctx = CLIContext.from_env()
    for key, value in kwargs.items():
        if value is not None and hasattr(key):
            setattr(ctx, key, value)
    return ctx


def x_create_cli_context__mutmut_7(**kwargs: Any) -> CLIContext:
    """Create a CLIContext for CLI usage.

    Loads from environment, then overlays any provided kwargs.

    Args:
        **kwargs: Override values for the context

    Returns:
        Configured CLIContext instance

    """
    ctx = CLIContext.from_env()
    for key, value in kwargs.items():
        if value is not None and hasattr(ctx, ):
            setattr(ctx, key, value)
    return ctx


def x_create_cli_context__mutmut_8(**kwargs: Any) -> CLIContext:
    """Create a CLIContext for CLI usage.

    Loads from environment, then overlays any provided kwargs.

    Args:
        **kwargs: Override values for the context

    Returns:
        Configured CLIContext instance

    """
    ctx = CLIContext.from_env()
    for key, value in kwargs.items():
        if value is not None and hasattr(ctx, key):
            setattr(None, key, value)
    return ctx


def x_create_cli_context__mutmut_9(**kwargs: Any) -> CLIContext:
    """Create a CLIContext for CLI usage.

    Loads from environment, then overlays any provided kwargs.

    Args:
        **kwargs: Override values for the context

    Returns:
        Configured CLIContext instance

    """
    ctx = CLIContext.from_env()
    for key, value in kwargs.items():
        if value is not None and hasattr(ctx, key):
            setattr(ctx, None, value)
    return ctx


def x_create_cli_context__mutmut_10(**kwargs: Any) -> CLIContext:
    """Create a CLIContext for CLI usage.

    Loads from environment, then overlays any provided kwargs.

    Args:
        **kwargs: Override values for the context

    Returns:
        Configured CLIContext instance

    """
    ctx = CLIContext.from_env()
    for key, value in kwargs.items():
        if value is not None and hasattr(ctx, key):
            setattr(ctx, key, None)
    return ctx


def x_create_cli_context__mutmut_11(**kwargs: Any) -> CLIContext:
    """Create a CLIContext for CLI usage.

    Loads from environment, then overlays any provided kwargs.

    Args:
        **kwargs: Override values for the context

    Returns:
        Configured CLIContext instance

    """
    ctx = CLIContext.from_env()
    for key, value in kwargs.items():
        if value is not None and hasattr(ctx, key):
            setattr(key, value)
    return ctx


def x_create_cli_context__mutmut_12(**kwargs: Any) -> CLIContext:
    """Create a CLIContext for CLI usage.

    Loads from environment, then overlays any provided kwargs.

    Args:
        **kwargs: Override values for the context

    Returns:
        Configured CLIContext instance

    """
    ctx = CLIContext.from_env()
    for key, value in kwargs.items():
        if value is not None and hasattr(ctx, key):
            setattr(ctx, value)
    return ctx


def x_create_cli_context__mutmut_13(**kwargs: Any) -> CLIContext:
    """Create a CLIContext for CLI usage.

    Loads from environment, then overlays any provided kwargs.

    Args:
        **kwargs: Override values for the context

    Returns:
        Configured CLIContext instance

    """
    ctx = CLIContext.from_env()
    for key, value in kwargs.items():
        if value is not None and hasattr(ctx, key):
            setattr(ctx, key, )
    return ctx

x_create_cli_context__mutmut_mutants : ClassVar[MutantDict] = {
'x_create_cli_context__mutmut_1': x_create_cli_context__mutmut_1, 
    'x_create_cli_context__mutmut_2': x_create_cli_context__mutmut_2, 
    'x_create_cli_context__mutmut_3': x_create_cli_context__mutmut_3, 
    'x_create_cli_context__mutmut_4': x_create_cli_context__mutmut_4, 
    'x_create_cli_context__mutmut_5': x_create_cli_context__mutmut_5, 
    'x_create_cli_context__mutmut_6': x_create_cli_context__mutmut_6, 
    'x_create_cli_context__mutmut_7': x_create_cli_context__mutmut_7, 
    'x_create_cli_context__mutmut_8': x_create_cli_context__mutmut_8, 
    'x_create_cli_context__mutmut_9': x_create_cli_context__mutmut_9, 
    'x_create_cli_context__mutmut_10': x_create_cli_context__mutmut_10, 
    'x_create_cli_context__mutmut_11': x_create_cli_context__mutmut_11, 
    'x_create_cli_context__mutmut_12': x_create_cli_context__mutmut_12, 
    'x_create_cli_context__mutmut_13': x_create_cli_context__mutmut_13
}

def create_cli_context(*args, **kwargs):
    result = _mutmut_trampoline(x_create_cli_context__mutmut_orig, x_create_cli_context__mutmut_mutants, args, kwargs)
    return result 

create_cli_context.__signature__ = _mutmut_signature(x_create_cli_context__mutmut_orig)
x_create_cli_context__mutmut_orig.__name__ = 'x_create_cli_context'


class CliTestRunner:
    """Test runner for CLI commands using Click's testing facilities."""

    def xǁCliTestRunnerǁ__init____mutmut_orig(self) -> None:
        self.runner = CliRunner()

    def xǁCliTestRunnerǁ__init____mutmut_1(self) -> None:
        self.runner = None
    
    xǁCliTestRunnerǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCliTestRunnerǁ__init____mutmut_1': xǁCliTestRunnerǁ__init____mutmut_1
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCliTestRunnerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁCliTestRunnerǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁCliTestRunnerǁ__init____mutmut_orig)
    xǁCliTestRunnerǁ__init____mutmut_orig.__name__ = 'xǁCliTestRunnerǁ__init__'

    def xǁCliTestRunnerǁinvoke__mutmut_orig(
        self,
        cli: click_types.Command | click_types.Group,
        args: list[str] | None = None,
        input: str | None = None,
        env: dict[str, str] | None = None,
        catch_exceptions: bool = True,
        **kwargs: Any,
    ) -> Result:
        """Invoke a CLI command for testing."""
        return self.runner.invoke(
            cli,
            args=args,
            input=input,
            env=env,
            catch_exceptions=catch_exceptions,
            **kwargs,
        )

    def xǁCliTestRunnerǁinvoke__mutmut_1(
        self,
        cli: click_types.Command | click_types.Group,
        args: list[str] | None = None,
        input: str | None = None,
        env: dict[str, str] | None = None,
        catch_exceptions: bool = False,
        **kwargs: Any,
    ) -> Result:
        """Invoke a CLI command for testing."""
        return self.runner.invoke(
            cli,
            args=args,
            input=input,
            env=env,
            catch_exceptions=catch_exceptions,
            **kwargs,
        )

    def xǁCliTestRunnerǁinvoke__mutmut_2(
        self,
        cli: click_types.Command | click_types.Group,
        args: list[str] | None = None,
        input: str | None = None,
        env: dict[str, str] | None = None,
        catch_exceptions: bool = True,
        **kwargs: Any,
    ) -> Result:
        """Invoke a CLI command for testing."""
        return self.runner.invoke(
            None,
            args=args,
            input=input,
            env=env,
            catch_exceptions=catch_exceptions,
            **kwargs,
        )

    def xǁCliTestRunnerǁinvoke__mutmut_3(
        self,
        cli: click_types.Command | click_types.Group,
        args: list[str] | None = None,
        input: str | None = None,
        env: dict[str, str] | None = None,
        catch_exceptions: bool = True,
        **kwargs: Any,
    ) -> Result:
        """Invoke a CLI command for testing."""
        return self.runner.invoke(
            cli,
            args=None,
            input=input,
            env=env,
            catch_exceptions=catch_exceptions,
            **kwargs,
        )

    def xǁCliTestRunnerǁinvoke__mutmut_4(
        self,
        cli: click_types.Command | click_types.Group,
        args: list[str] | None = None,
        input: str | None = None,
        env: dict[str, str] | None = None,
        catch_exceptions: bool = True,
        **kwargs: Any,
    ) -> Result:
        """Invoke a CLI command for testing."""
        return self.runner.invoke(
            cli,
            args=args,
            input=None,
            env=env,
            catch_exceptions=catch_exceptions,
            **kwargs,
        )

    def xǁCliTestRunnerǁinvoke__mutmut_5(
        self,
        cli: click_types.Command | click_types.Group,
        args: list[str] | None = None,
        input: str | None = None,
        env: dict[str, str] | None = None,
        catch_exceptions: bool = True,
        **kwargs: Any,
    ) -> Result:
        """Invoke a CLI command for testing."""
        return self.runner.invoke(
            cli,
            args=args,
            input=input,
            env=None,
            catch_exceptions=catch_exceptions,
            **kwargs,
        )

    def xǁCliTestRunnerǁinvoke__mutmut_6(
        self,
        cli: click_types.Command | click_types.Group,
        args: list[str] | None = None,
        input: str | None = None,
        env: dict[str, str] | None = None,
        catch_exceptions: bool = True,
        **kwargs: Any,
    ) -> Result:
        """Invoke a CLI command for testing."""
        return self.runner.invoke(
            cli,
            args=args,
            input=input,
            env=env,
            catch_exceptions=None,
            **kwargs,
        )

    def xǁCliTestRunnerǁinvoke__mutmut_7(
        self,
        cli: click_types.Command | click_types.Group,
        args: list[str] | None = None,
        input: str | None = None,
        env: dict[str, str] | None = None,
        catch_exceptions: bool = True,
        **kwargs: Any,
    ) -> Result:
        """Invoke a CLI command for testing."""
        return self.runner.invoke(
            args=args,
            input=input,
            env=env,
            catch_exceptions=catch_exceptions,
            **kwargs,
        )

    def xǁCliTestRunnerǁinvoke__mutmut_8(
        self,
        cli: click_types.Command | click_types.Group,
        args: list[str] | None = None,
        input: str | None = None,
        env: dict[str, str] | None = None,
        catch_exceptions: bool = True,
        **kwargs: Any,
    ) -> Result:
        """Invoke a CLI command for testing."""
        return self.runner.invoke(
            cli,
            input=input,
            env=env,
            catch_exceptions=catch_exceptions,
            **kwargs,
        )

    def xǁCliTestRunnerǁinvoke__mutmut_9(
        self,
        cli: click_types.Command | click_types.Group,
        args: list[str] | None = None,
        input: str | None = None,
        env: dict[str, str] | None = None,
        catch_exceptions: bool = True,
        **kwargs: Any,
    ) -> Result:
        """Invoke a CLI command for testing."""
        return self.runner.invoke(
            cli,
            args=args,
            env=env,
            catch_exceptions=catch_exceptions,
            **kwargs,
        )

    def xǁCliTestRunnerǁinvoke__mutmut_10(
        self,
        cli: click_types.Command | click_types.Group,
        args: list[str] | None = None,
        input: str | None = None,
        env: dict[str, str] | None = None,
        catch_exceptions: bool = True,
        **kwargs: Any,
    ) -> Result:
        """Invoke a CLI command for testing."""
        return self.runner.invoke(
            cli,
            args=args,
            input=input,
            catch_exceptions=catch_exceptions,
            **kwargs,
        )

    def xǁCliTestRunnerǁinvoke__mutmut_11(
        self,
        cli: click_types.Command | click_types.Group,
        args: list[str] | None = None,
        input: str | None = None,
        env: dict[str, str] | None = None,
        catch_exceptions: bool = True,
        **kwargs: Any,
    ) -> Result:
        """Invoke a CLI command for testing."""
        return self.runner.invoke(
            cli,
            args=args,
            input=input,
            env=env,
            **kwargs,
        )

    def xǁCliTestRunnerǁinvoke__mutmut_12(
        self,
        cli: click_types.Command | click_types.Group,
        args: list[str] | None = None,
        input: str | None = None,
        env: dict[str, str] | None = None,
        catch_exceptions: bool = True,
        **kwargs: Any,
    ) -> Result:
        """Invoke a CLI command for testing."""
        return self.runner.invoke(
            cli,
            args=args,
            input=input,
            env=env,
            catch_exceptions=catch_exceptions,
            )
    
    xǁCliTestRunnerǁinvoke__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCliTestRunnerǁinvoke__mutmut_1': xǁCliTestRunnerǁinvoke__mutmut_1, 
        'xǁCliTestRunnerǁinvoke__mutmut_2': xǁCliTestRunnerǁinvoke__mutmut_2, 
        'xǁCliTestRunnerǁinvoke__mutmut_3': xǁCliTestRunnerǁinvoke__mutmut_3, 
        'xǁCliTestRunnerǁinvoke__mutmut_4': xǁCliTestRunnerǁinvoke__mutmut_4, 
        'xǁCliTestRunnerǁinvoke__mutmut_5': xǁCliTestRunnerǁinvoke__mutmut_5, 
        'xǁCliTestRunnerǁinvoke__mutmut_6': xǁCliTestRunnerǁinvoke__mutmut_6, 
        'xǁCliTestRunnerǁinvoke__mutmut_7': xǁCliTestRunnerǁinvoke__mutmut_7, 
        'xǁCliTestRunnerǁinvoke__mutmut_8': xǁCliTestRunnerǁinvoke__mutmut_8, 
        'xǁCliTestRunnerǁinvoke__mutmut_9': xǁCliTestRunnerǁinvoke__mutmut_9, 
        'xǁCliTestRunnerǁinvoke__mutmut_10': xǁCliTestRunnerǁinvoke__mutmut_10, 
        'xǁCliTestRunnerǁinvoke__mutmut_11': xǁCliTestRunnerǁinvoke__mutmut_11, 
        'xǁCliTestRunnerǁinvoke__mutmut_12': xǁCliTestRunnerǁinvoke__mutmut_12
    }
    
    def invoke(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCliTestRunnerǁinvoke__mutmut_orig"), object.__getattribute__(self, "xǁCliTestRunnerǁinvoke__mutmut_mutants"), args, kwargs, self)
        return result 
    
    invoke.__signature__ = _mutmut_signature(xǁCliTestRunnerǁinvoke__mutmut_orig)
    xǁCliTestRunnerǁinvoke__mutmut_orig.__name__ = 'xǁCliTestRunnerǁinvoke'

    def isolated_filesystem(self) -> object:
        """Context manager for isolated filesystem."""
        return self.runner.isolated_filesystem()


def x_assert_cli_success__mutmut_orig(result: Result, expected_output: str | None = None) -> None:
    """Assert that a CLI command succeeded."""
    if result.exit_code != 0:
        raise AssertionError(
            f"Command failed with exit code {result.exit_code}\n"
            f"Output: {result.output}\n"
            f"Exception: {result.exception}",
        )

    if expected_output and expected_output not in result.output:
        raise AssertionError(
            f"Expected output not found.\nExpected: {expected_output}\nActual: {result.output}",
        )


def x_assert_cli_success__mutmut_1(result: Result, expected_output: str | None = None) -> None:
    """Assert that a CLI command succeeded."""
    if result.exit_code == 0:
        raise AssertionError(
            f"Command failed with exit code {result.exit_code}\n"
            f"Output: {result.output}\n"
            f"Exception: {result.exception}",
        )

    if expected_output and expected_output not in result.output:
        raise AssertionError(
            f"Expected output not found.\nExpected: {expected_output}\nActual: {result.output}",
        )


def x_assert_cli_success__mutmut_2(result: Result, expected_output: str | None = None) -> None:
    """Assert that a CLI command succeeded."""
    if result.exit_code != 1:
        raise AssertionError(
            f"Command failed with exit code {result.exit_code}\n"
            f"Output: {result.output}\n"
            f"Exception: {result.exception}",
        )

    if expected_output and expected_output not in result.output:
        raise AssertionError(
            f"Expected output not found.\nExpected: {expected_output}\nActual: {result.output}",
        )


def x_assert_cli_success__mutmut_3(result: Result, expected_output: str | None = None) -> None:
    """Assert that a CLI command succeeded."""
    if result.exit_code != 0:
        raise AssertionError(
            None,
        )

    if expected_output and expected_output not in result.output:
        raise AssertionError(
            f"Expected output not found.\nExpected: {expected_output}\nActual: {result.output}",
        )


def x_assert_cli_success__mutmut_4(result: Result, expected_output: str | None = None) -> None:
    """Assert that a CLI command succeeded."""
    if result.exit_code != 0:
        raise AssertionError(
            f"Command failed with exit code {result.exit_code}\n"
            f"Output: {result.output}\n"
            f"Exception: {result.exception}",
        )

    if expected_output or expected_output not in result.output:
        raise AssertionError(
            f"Expected output not found.\nExpected: {expected_output}\nActual: {result.output}",
        )


def x_assert_cli_success__mutmut_5(result: Result, expected_output: str | None = None) -> None:
    """Assert that a CLI command succeeded."""
    if result.exit_code != 0:
        raise AssertionError(
            f"Command failed with exit code {result.exit_code}\n"
            f"Output: {result.output}\n"
            f"Exception: {result.exception}",
        )

    if expected_output and expected_output in result.output:
        raise AssertionError(
            f"Expected output not found.\nExpected: {expected_output}\nActual: {result.output}",
        )


def x_assert_cli_success__mutmut_6(result: Result, expected_output: str | None = None) -> None:
    """Assert that a CLI command succeeded."""
    if result.exit_code != 0:
        raise AssertionError(
            f"Command failed with exit code {result.exit_code}\n"
            f"Output: {result.output}\n"
            f"Exception: {result.exception}",
        )

    if expected_output and expected_output not in result.output:
        raise AssertionError(
            None,
        )

x_assert_cli_success__mutmut_mutants : ClassVar[MutantDict] = {
'x_assert_cli_success__mutmut_1': x_assert_cli_success__mutmut_1, 
    'x_assert_cli_success__mutmut_2': x_assert_cli_success__mutmut_2, 
    'x_assert_cli_success__mutmut_3': x_assert_cli_success__mutmut_3, 
    'x_assert_cli_success__mutmut_4': x_assert_cli_success__mutmut_4, 
    'x_assert_cli_success__mutmut_5': x_assert_cli_success__mutmut_5, 
    'x_assert_cli_success__mutmut_6': x_assert_cli_success__mutmut_6
}

def assert_cli_success(*args, **kwargs):
    result = _mutmut_trampoline(x_assert_cli_success__mutmut_orig, x_assert_cli_success__mutmut_mutants, args, kwargs)
    return result 

assert_cli_success.__signature__ = _mutmut_signature(x_assert_cli_success__mutmut_orig)
x_assert_cli_success__mutmut_orig.__name__ = 'x_assert_cli_success'


def x_assert_cli_error__mutmut_orig(
    result: Result,
    expected_error: str | None = None,
    exit_code: int | None = None,
) -> None:
    """Assert that a CLI command failed."""
    if result.exit_code == 0:
        raise AssertionError(f"Command succeeded unexpectedly\nOutput: {result.output}")

    if exit_code is not None and result.exit_code != exit_code:
        raise AssertionError(f"Wrong exit code.\nExpected: {exit_code}\nActual: {result.exit_code}")

    if expected_error and expected_error not in result.output:
        raise AssertionError(f"Expected error not found.\nExpected: {expected_error}\nActual: {result.output}")


def x_assert_cli_error__mutmut_1(
    result: Result,
    expected_error: str | None = None,
    exit_code: int | None = None,
) -> None:
    """Assert that a CLI command failed."""
    if result.exit_code != 0:
        raise AssertionError(f"Command succeeded unexpectedly\nOutput: {result.output}")

    if exit_code is not None and result.exit_code != exit_code:
        raise AssertionError(f"Wrong exit code.\nExpected: {exit_code}\nActual: {result.exit_code}")

    if expected_error and expected_error not in result.output:
        raise AssertionError(f"Expected error not found.\nExpected: {expected_error}\nActual: {result.output}")


def x_assert_cli_error__mutmut_2(
    result: Result,
    expected_error: str | None = None,
    exit_code: int | None = None,
) -> None:
    """Assert that a CLI command failed."""
    if result.exit_code == 1:
        raise AssertionError(f"Command succeeded unexpectedly\nOutput: {result.output}")

    if exit_code is not None and result.exit_code != exit_code:
        raise AssertionError(f"Wrong exit code.\nExpected: {exit_code}\nActual: {result.exit_code}")

    if expected_error and expected_error not in result.output:
        raise AssertionError(f"Expected error not found.\nExpected: {expected_error}\nActual: {result.output}")


def x_assert_cli_error__mutmut_3(
    result: Result,
    expected_error: str | None = None,
    exit_code: int | None = None,
) -> None:
    """Assert that a CLI command failed."""
    if result.exit_code == 0:
        raise AssertionError(None)

    if exit_code is not None and result.exit_code != exit_code:
        raise AssertionError(f"Wrong exit code.\nExpected: {exit_code}\nActual: {result.exit_code}")

    if expected_error and expected_error not in result.output:
        raise AssertionError(f"Expected error not found.\nExpected: {expected_error}\nActual: {result.output}")


def x_assert_cli_error__mutmut_4(
    result: Result,
    expected_error: str | None = None,
    exit_code: int | None = None,
) -> None:
    """Assert that a CLI command failed."""
    if result.exit_code == 0:
        raise AssertionError(f"Command succeeded unexpectedly\nOutput: {result.output}")

    if exit_code is not None or result.exit_code != exit_code:
        raise AssertionError(f"Wrong exit code.\nExpected: {exit_code}\nActual: {result.exit_code}")

    if expected_error and expected_error not in result.output:
        raise AssertionError(f"Expected error not found.\nExpected: {expected_error}\nActual: {result.output}")


def x_assert_cli_error__mutmut_5(
    result: Result,
    expected_error: str | None = None,
    exit_code: int | None = None,
) -> None:
    """Assert that a CLI command failed."""
    if result.exit_code == 0:
        raise AssertionError(f"Command succeeded unexpectedly\nOutput: {result.output}")

    if exit_code is None and result.exit_code != exit_code:
        raise AssertionError(f"Wrong exit code.\nExpected: {exit_code}\nActual: {result.exit_code}")

    if expected_error and expected_error not in result.output:
        raise AssertionError(f"Expected error not found.\nExpected: {expected_error}\nActual: {result.output}")


def x_assert_cli_error__mutmut_6(
    result: Result,
    expected_error: str | None = None,
    exit_code: int | None = None,
) -> None:
    """Assert that a CLI command failed."""
    if result.exit_code == 0:
        raise AssertionError(f"Command succeeded unexpectedly\nOutput: {result.output}")

    if exit_code is not None and result.exit_code == exit_code:
        raise AssertionError(f"Wrong exit code.\nExpected: {exit_code}\nActual: {result.exit_code}")

    if expected_error and expected_error not in result.output:
        raise AssertionError(f"Expected error not found.\nExpected: {expected_error}\nActual: {result.output}")


def x_assert_cli_error__mutmut_7(
    result: Result,
    expected_error: str | None = None,
    exit_code: int | None = None,
) -> None:
    """Assert that a CLI command failed."""
    if result.exit_code == 0:
        raise AssertionError(f"Command succeeded unexpectedly\nOutput: {result.output}")

    if exit_code is not None and result.exit_code != exit_code:
        raise AssertionError(None)

    if expected_error and expected_error not in result.output:
        raise AssertionError(f"Expected error not found.\nExpected: {expected_error}\nActual: {result.output}")


def x_assert_cli_error__mutmut_8(
    result: Result,
    expected_error: str | None = None,
    exit_code: int | None = None,
) -> None:
    """Assert that a CLI command failed."""
    if result.exit_code == 0:
        raise AssertionError(f"Command succeeded unexpectedly\nOutput: {result.output}")

    if exit_code is not None and result.exit_code != exit_code:
        raise AssertionError(f"Wrong exit code.\nExpected: {exit_code}\nActual: {result.exit_code}")

    if expected_error or expected_error not in result.output:
        raise AssertionError(f"Expected error not found.\nExpected: {expected_error}\nActual: {result.output}")


def x_assert_cli_error__mutmut_9(
    result: Result,
    expected_error: str | None = None,
    exit_code: int | None = None,
) -> None:
    """Assert that a CLI command failed."""
    if result.exit_code == 0:
        raise AssertionError(f"Command succeeded unexpectedly\nOutput: {result.output}")

    if exit_code is not None and result.exit_code != exit_code:
        raise AssertionError(f"Wrong exit code.\nExpected: {exit_code}\nActual: {result.exit_code}")

    if expected_error and expected_error in result.output:
        raise AssertionError(f"Expected error not found.\nExpected: {expected_error}\nActual: {result.output}")


def x_assert_cli_error__mutmut_10(
    result: Result,
    expected_error: str | None = None,
    exit_code: int | None = None,
) -> None:
    """Assert that a CLI command failed."""
    if result.exit_code == 0:
        raise AssertionError(f"Command succeeded unexpectedly\nOutput: {result.output}")

    if exit_code is not None and result.exit_code != exit_code:
        raise AssertionError(f"Wrong exit code.\nExpected: {exit_code}\nActual: {result.exit_code}")

    if expected_error and expected_error not in result.output:
        raise AssertionError(None)

x_assert_cli_error__mutmut_mutants : ClassVar[MutantDict] = {
'x_assert_cli_error__mutmut_1': x_assert_cli_error__mutmut_1, 
    'x_assert_cli_error__mutmut_2': x_assert_cli_error__mutmut_2, 
    'x_assert_cli_error__mutmut_3': x_assert_cli_error__mutmut_3, 
    'x_assert_cli_error__mutmut_4': x_assert_cli_error__mutmut_4, 
    'x_assert_cli_error__mutmut_5': x_assert_cli_error__mutmut_5, 
    'x_assert_cli_error__mutmut_6': x_assert_cli_error__mutmut_6, 
    'x_assert_cli_error__mutmut_7': x_assert_cli_error__mutmut_7, 
    'x_assert_cli_error__mutmut_8': x_assert_cli_error__mutmut_8, 
    'x_assert_cli_error__mutmut_9': x_assert_cli_error__mutmut_9, 
    'x_assert_cli_error__mutmut_10': x_assert_cli_error__mutmut_10
}

def assert_cli_error(*args, **kwargs):
    result = _mutmut_trampoline(x_assert_cli_error__mutmut_orig, x_assert_cli_error__mutmut_mutants, args, kwargs)
    return result 

assert_cli_error.__signature__ = _mutmut_signature(x_assert_cli_error__mutmut_orig)
x_assert_cli_error__mutmut_orig.__name__ = 'x_assert_cli_error'


# <3 🧱🤝💻🪄
