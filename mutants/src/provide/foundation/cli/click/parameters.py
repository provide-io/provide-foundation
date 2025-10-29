# provide/foundation/cli/click/parameters.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Click parameter processing and decorator application.

Handles separation of arguments/options and application of Click decorators
based on parameter introspection and type hints.
"""

from __future__ import annotations

from typing import Any

from provide.foundation.cli.deps import click
from provide.foundation.hub.introspection import ParameterInfo

__all__ = [
    "apply_click_argument",
    "apply_click_option",
    "separate_arguments_and_options",
]
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


def x_separate_arguments_and_options__mutmut_orig(
    params: list[ParameterInfo],
    force_options: bool = False,
) -> tuple[list[ParameterInfo], list[ParameterInfo]]:
    """Separate parameters into arguments and options using Position-Based Hybrid.

    Rules:
    1. Explicit cli_hint='argument' → argument (even with default)
    2. Explicit cli_hint='option' → option (even without default)
    3. No hint + no default → argument
    4. No hint + has default + bool → option (flag)
    5. No hint + has default + non-bool → first becomes optional argument, rest become options
       (unless force_options=True, then all become options)

    Position-Based Hybrid provides natural UX:
    - First parameter feels like the "main thing" → optional positional argument
    - Additional parameters → explicit flags
    - Boolean parameters → always flags

    Example:
        def send(message: str = None, level: str = "INFO", verbose: bool = False):
            ...

        Becomes CLI:
            send [MESSAGE] --level INFO --verbose

        With force_options=True:
            send --message TEXT --level INFO --verbose

    Args:
        params: List of ParameterInfo objects
        force_options: If True, all parameters with defaults become options
                      (disables Position-Based Hybrid for first parameter)

    Returns:
        (arguments, options) tuple of parameter lists

    """
    arguments = []
    options = []

    for param in params:
        if param.cli_hint == "argument":
            # Explicitly marked as argument
            arguments.append(param)
        elif param.cli_hint == "option":
            # Explicitly marked as option
            options.append(param)
        elif not param.has_default:
            # No explicit hint, no default → argument
            arguments.append(param)
        elif param.concrete_type is bool:
            # Boolean parameters always become flags
            options.append(param)
        else:
            # Has default, non-boolean → Position-Based Hybrid
            # First param becomes optional argument, rest become options
            # (unless force_options is True)
            if force_options or arguments or options:
                # force_options enabled OR subsequent parameters → make them options
                options.append(param)
            else:
                # First parameter overall → make it an optional argument
                arguments.append(param)

    return arguments, options


def x_separate_arguments_and_options__mutmut_1(
    params: list[ParameterInfo],
    force_options: bool = True,
) -> tuple[list[ParameterInfo], list[ParameterInfo]]:
    """Separate parameters into arguments and options using Position-Based Hybrid.

    Rules:
    1. Explicit cli_hint='argument' → argument (even with default)
    2. Explicit cli_hint='option' → option (even without default)
    3. No hint + no default → argument
    4. No hint + has default + bool → option (flag)
    5. No hint + has default + non-bool → first becomes optional argument, rest become options
       (unless force_options=True, then all become options)

    Position-Based Hybrid provides natural UX:
    - First parameter feels like the "main thing" → optional positional argument
    - Additional parameters → explicit flags
    - Boolean parameters → always flags

    Example:
        def send(message: str = None, level: str = "INFO", verbose: bool = False):
            ...

        Becomes CLI:
            send [MESSAGE] --level INFO --verbose

        With force_options=True:
            send --message TEXT --level INFO --verbose

    Args:
        params: List of ParameterInfo objects
        force_options: If True, all parameters with defaults become options
                      (disables Position-Based Hybrid for first parameter)

    Returns:
        (arguments, options) tuple of parameter lists

    """
    arguments = []
    options = []

    for param in params:
        if param.cli_hint == "argument":
            # Explicitly marked as argument
            arguments.append(param)
        elif param.cli_hint == "option":
            # Explicitly marked as option
            options.append(param)
        elif not param.has_default:
            # No explicit hint, no default → argument
            arguments.append(param)
        elif param.concrete_type is bool:
            # Boolean parameters always become flags
            options.append(param)
        else:
            # Has default, non-boolean → Position-Based Hybrid
            # First param becomes optional argument, rest become options
            # (unless force_options is True)
            if force_options or arguments or options:
                # force_options enabled OR subsequent parameters → make them options
                options.append(param)
            else:
                # First parameter overall → make it an optional argument
                arguments.append(param)

    return arguments, options


def x_separate_arguments_and_options__mutmut_2(
    params: list[ParameterInfo],
    force_options: bool = False,
) -> tuple[list[ParameterInfo], list[ParameterInfo]]:
    """Separate parameters into arguments and options using Position-Based Hybrid.

    Rules:
    1. Explicit cli_hint='argument' → argument (even with default)
    2. Explicit cli_hint='option' → option (even without default)
    3. No hint + no default → argument
    4. No hint + has default + bool → option (flag)
    5. No hint + has default + non-bool → first becomes optional argument, rest become options
       (unless force_options=True, then all become options)

    Position-Based Hybrid provides natural UX:
    - First parameter feels like the "main thing" → optional positional argument
    - Additional parameters → explicit flags
    - Boolean parameters → always flags

    Example:
        def send(message: str = None, level: str = "INFO", verbose: bool = False):
            ...

        Becomes CLI:
            send [MESSAGE] --level INFO --verbose

        With force_options=True:
            send --message TEXT --level INFO --verbose

    Args:
        params: List of ParameterInfo objects
        force_options: If True, all parameters with defaults become options
                      (disables Position-Based Hybrid for first parameter)

    Returns:
        (arguments, options) tuple of parameter lists

    """
    arguments = None
    options = []

    for param in params:
        if param.cli_hint == "argument":
            # Explicitly marked as argument
            arguments.append(param)
        elif param.cli_hint == "option":
            # Explicitly marked as option
            options.append(param)
        elif not param.has_default:
            # No explicit hint, no default → argument
            arguments.append(param)
        elif param.concrete_type is bool:
            # Boolean parameters always become flags
            options.append(param)
        else:
            # Has default, non-boolean → Position-Based Hybrid
            # First param becomes optional argument, rest become options
            # (unless force_options is True)
            if force_options or arguments or options:
                # force_options enabled OR subsequent parameters → make them options
                options.append(param)
            else:
                # First parameter overall → make it an optional argument
                arguments.append(param)

    return arguments, options


def x_separate_arguments_and_options__mutmut_3(
    params: list[ParameterInfo],
    force_options: bool = False,
) -> tuple[list[ParameterInfo], list[ParameterInfo]]:
    """Separate parameters into arguments and options using Position-Based Hybrid.

    Rules:
    1. Explicit cli_hint='argument' → argument (even with default)
    2. Explicit cli_hint='option' → option (even without default)
    3. No hint + no default → argument
    4. No hint + has default + bool → option (flag)
    5. No hint + has default + non-bool → first becomes optional argument, rest become options
       (unless force_options=True, then all become options)

    Position-Based Hybrid provides natural UX:
    - First parameter feels like the "main thing" → optional positional argument
    - Additional parameters → explicit flags
    - Boolean parameters → always flags

    Example:
        def send(message: str = None, level: str = "INFO", verbose: bool = False):
            ...

        Becomes CLI:
            send [MESSAGE] --level INFO --verbose

        With force_options=True:
            send --message TEXT --level INFO --verbose

    Args:
        params: List of ParameterInfo objects
        force_options: If True, all parameters with defaults become options
                      (disables Position-Based Hybrid for first parameter)

    Returns:
        (arguments, options) tuple of parameter lists

    """
    arguments = []
    options = None

    for param in params:
        if param.cli_hint == "argument":
            # Explicitly marked as argument
            arguments.append(param)
        elif param.cli_hint == "option":
            # Explicitly marked as option
            options.append(param)
        elif not param.has_default:
            # No explicit hint, no default → argument
            arguments.append(param)
        elif param.concrete_type is bool:
            # Boolean parameters always become flags
            options.append(param)
        else:
            # Has default, non-boolean → Position-Based Hybrid
            # First param becomes optional argument, rest become options
            # (unless force_options is True)
            if force_options or arguments or options:
                # force_options enabled OR subsequent parameters → make them options
                options.append(param)
            else:
                # First parameter overall → make it an optional argument
                arguments.append(param)

    return arguments, options


def x_separate_arguments_and_options__mutmut_4(
    params: list[ParameterInfo],
    force_options: bool = False,
) -> tuple[list[ParameterInfo], list[ParameterInfo]]:
    """Separate parameters into arguments and options using Position-Based Hybrid.

    Rules:
    1. Explicit cli_hint='argument' → argument (even with default)
    2. Explicit cli_hint='option' → option (even without default)
    3. No hint + no default → argument
    4. No hint + has default + bool → option (flag)
    5. No hint + has default + non-bool → first becomes optional argument, rest become options
       (unless force_options=True, then all become options)

    Position-Based Hybrid provides natural UX:
    - First parameter feels like the "main thing" → optional positional argument
    - Additional parameters → explicit flags
    - Boolean parameters → always flags

    Example:
        def send(message: str = None, level: str = "INFO", verbose: bool = False):
            ...

        Becomes CLI:
            send [MESSAGE] --level INFO --verbose

        With force_options=True:
            send --message TEXT --level INFO --verbose

    Args:
        params: List of ParameterInfo objects
        force_options: If True, all parameters with defaults become options
                      (disables Position-Based Hybrid for first parameter)

    Returns:
        (arguments, options) tuple of parameter lists

    """
    arguments = []
    options = []

    for param in params:
        if param.cli_hint != "argument":
            # Explicitly marked as argument
            arguments.append(param)
        elif param.cli_hint == "option":
            # Explicitly marked as option
            options.append(param)
        elif not param.has_default:
            # No explicit hint, no default → argument
            arguments.append(param)
        elif param.concrete_type is bool:
            # Boolean parameters always become flags
            options.append(param)
        else:
            # Has default, non-boolean → Position-Based Hybrid
            # First param becomes optional argument, rest become options
            # (unless force_options is True)
            if force_options or arguments or options:
                # force_options enabled OR subsequent parameters → make them options
                options.append(param)
            else:
                # First parameter overall → make it an optional argument
                arguments.append(param)

    return arguments, options


def x_separate_arguments_and_options__mutmut_5(
    params: list[ParameterInfo],
    force_options: bool = False,
) -> tuple[list[ParameterInfo], list[ParameterInfo]]:
    """Separate parameters into arguments and options using Position-Based Hybrid.

    Rules:
    1. Explicit cli_hint='argument' → argument (even with default)
    2. Explicit cli_hint='option' → option (even without default)
    3. No hint + no default → argument
    4. No hint + has default + bool → option (flag)
    5. No hint + has default + non-bool → first becomes optional argument, rest become options
       (unless force_options=True, then all become options)

    Position-Based Hybrid provides natural UX:
    - First parameter feels like the "main thing" → optional positional argument
    - Additional parameters → explicit flags
    - Boolean parameters → always flags

    Example:
        def send(message: str = None, level: str = "INFO", verbose: bool = False):
            ...

        Becomes CLI:
            send [MESSAGE] --level INFO --verbose

        With force_options=True:
            send --message TEXT --level INFO --verbose

    Args:
        params: List of ParameterInfo objects
        force_options: If True, all parameters with defaults become options
                      (disables Position-Based Hybrid for first parameter)

    Returns:
        (arguments, options) tuple of parameter lists

    """
    arguments = []
    options = []

    for param in params:
        if param.cli_hint == "XXargumentXX":
            # Explicitly marked as argument
            arguments.append(param)
        elif param.cli_hint == "option":
            # Explicitly marked as option
            options.append(param)
        elif not param.has_default:
            # No explicit hint, no default → argument
            arguments.append(param)
        elif param.concrete_type is bool:
            # Boolean parameters always become flags
            options.append(param)
        else:
            # Has default, non-boolean → Position-Based Hybrid
            # First param becomes optional argument, rest become options
            # (unless force_options is True)
            if force_options or arguments or options:
                # force_options enabled OR subsequent parameters → make them options
                options.append(param)
            else:
                # First parameter overall → make it an optional argument
                arguments.append(param)

    return arguments, options


def x_separate_arguments_and_options__mutmut_6(
    params: list[ParameterInfo],
    force_options: bool = False,
) -> tuple[list[ParameterInfo], list[ParameterInfo]]:
    """Separate parameters into arguments and options using Position-Based Hybrid.

    Rules:
    1. Explicit cli_hint='argument' → argument (even with default)
    2. Explicit cli_hint='option' → option (even without default)
    3. No hint + no default → argument
    4. No hint + has default + bool → option (flag)
    5. No hint + has default + non-bool → first becomes optional argument, rest become options
       (unless force_options=True, then all become options)

    Position-Based Hybrid provides natural UX:
    - First parameter feels like the "main thing" → optional positional argument
    - Additional parameters → explicit flags
    - Boolean parameters → always flags

    Example:
        def send(message: str = None, level: str = "INFO", verbose: bool = False):
            ...

        Becomes CLI:
            send [MESSAGE] --level INFO --verbose

        With force_options=True:
            send --message TEXT --level INFO --verbose

    Args:
        params: List of ParameterInfo objects
        force_options: If True, all parameters with defaults become options
                      (disables Position-Based Hybrid for first parameter)

    Returns:
        (arguments, options) tuple of parameter lists

    """
    arguments = []
    options = []

    for param in params:
        if param.cli_hint == "ARGUMENT":
            # Explicitly marked as argument
            arguments.append(param)
        elif param.cli_hint == "option":
            # Explicitly marked as option
            options.append(param)
        elif not param.has_default:
            # No explicit hint, no default → argument
            arguments.append(param)
        elif param.concrete_type is bool:
            # Boolean parameters always become flags
            options.append(param)
        else:
            # Has default, non-boolean → Position-Based Hybrid
            # First param becomes optional argument, rest become options
            # (unless force_options is True)
            if force_options or arguments or options:
                # force_options enabled OR subsequent parameters → make them options
                options.append(param)
            else:
                # First parameter overall → make it an optional argument
                arguments.append(param)

    return arguments, options


def x_separate_arguments_and_options__mutmut_7(
    params: list[ParameterInfo],
    force_options: bool = False,
) -> tuple[list[ParameterInfo], list[ParameterInfo]]:
    """Separate parameters into arguments and options using Position-Based Hybrid.

    Rules:
    1. Explicit cli_hint='argument' → argument (even with default)
    2. Explicit cli_hint='option' → option (even without default)
    3. No hint + no default → argument
    4. No hint + has default + bool → option (flag)
    5. No hint + has default + non-bool → first becomes optional argument, rest become options
       (unless force_options=True, then all become options)

    Position-Based Hybrid provides natural UX:
    - First parameter feels like the "main thing" → optional positional argument
    - Additional parameters → explicit flags
    - Boolean parameters → always flags

    Example:
        def send(message: str = None, level: str = "INFO", verbose: bool = False):
            ...

        Becomes CLI:
            send [MESSAGE] --level INFO --verbose

        With force_options=True:
            send --message TEXT --level INFO --verbose

    Args:
        params: List of ParameterInfo objects
        force_options: If True, all parameters with defaults become options
                      (disables Position-Based Hybrid for first parameter)

    Returns:
        (arguments, options) tuple of parameter lists

    """
    arguments = []
    options = []

    for param in params:
        if param.cli_hint == "argument":
            # Explicitly marked as argument
            arguments.append(None)
        elif param.cli_hint == "option":
            # Explicitly marked as option
            options.append(param)
        elif not param.has_default:
            # No explicit hint, no default → argument
            arguments.append(param)
        elif param.concrete_type is bool:
            # Boolean parameters always become flags
            options.append(param)
        else:
            # Has default, non-boolean → Position-Based Hybrid
            # First param becomes optional argument, rest become options
            # (unless force_options is True)
            if force_options or arguments or options:
                # force_options enabled OR subsequent parameters → make them options
                options.append(param)
            else:
                # First parameter overall → make it an optional argument
                arguments.append(param)

    return arguments, options


def x_separate_arguments_and_options__mutmut_8(
    params: list[ParameterInfo],
    force_options: bool = False,
) -> tuple[list[ParameterInfo], list[ParameterInfo]]:
    """Separate parameters into arguments and options using Position-Based Hybrid.

    Rules:
    1. Explicit cli_hint='argument' → argument (even with default)
    2. Explicit cli_hint='option' → option (even without default)
    3. No hint + no default → argument
    4. No hint + has default + bool → option (flag)
    5. No hint + has default + non-bool → first becomes optional argument, rest become options
       (unless force_options=True, then all become options)

    Position-Based Hybrid provides natural UX:
    - First parameter feels like the "main thing" → optional positional argument
    - Additional parameters → explicit flags
    - Boolean parameters → always flags

    Example:
        def send(message: str = None, level: str = "INFO", verbose: bool = False):
            ...

        Becomes CLI:
            send [MESSAGE] --level INFO --verbose

        With force_options=True:
            send --message TEXT --level INFO --verbose

    Args:
        params: List of ParameterInfo objects
        force_options: If True, all parameters with defaults become options
                      (disables Position-Based Hybrid for first parameter)

    Returns:
        (arguments, options) tuple of parameter lists

    """
    arguments = []
    options = []

    for param in params:
        if param.cli_hint == "argument":
            # Explicitly marked as argument
            arguments.append(param)
        elif param.cli_hint != "option":
            # Explicitly marked as option
            options.append(param)
        elif not param.has_default:
            # No explicit hint, no default → argument
            arguments.append(param)
        elif param.concrete_type is bool:
            # Boolean parameters always become flags
            options.append(param)
        else:
            # Has default, non-boolean → Position-Based Hybrid
            # First param becomes optional argument, rest become options
            # (unless force_options is True)
            if force_options or arguments or options:
                # force_options enabled OR subsequent parameters → make them options
                options.append(param)
            else:
                # First parameter overall → make it an optional argument
                arguments.append(param)

    return arguments, options


def x_separate_arguments_and_options__mutmut_9(
    params: list[ParameterInfo],
    force_options: bool = False,
) -> tuple[list[ParameterInfo], list[ParameterInfo]]:
    """Separate parameters into arguments and options using Position-Based Hybrid.

    Rules:
    1. Explicit cli_hint='argument' → argument (even with default)
    2. Explicit cli_hint='option' → option (even without default)
    3. No hint + no default → argument
    4. No hint + has default + bool → option (flag)
    5. No hint + has default + non-bool → first becomes optional argument, rest become options
       (unless force_options=True, then all become options)

    Position-Based Hybrid provides natural UX:
    - First parameter feels like the "main thing" → optional positional argument
    - Additional parameters → explicit flags
    - Boolean parameters → always flags

    Example:
        def send(message: str = None, level: str = "INFO", verbose: bool = False):
            ...

        Becomes CLI:
            send [MESSAGE] --level INFO --verbose

        With force_options=True:
            send --message TEXT --level INFO --verbose

    Args:
        params: List of ParameterInfo objects
        force_options: If True, all parameters with defaults become options
                      (disables Position-Based Hybrid for first parameter)

    Returns:
        (arguments, options) tuple of parameter lists

    """
    arguments = []
    options = []

    for param in params:
        if param.cli_hint == "argument":
            # Explicitly marked as argument
            arguments.append(param)
        elif param.cli_hint == "XXoptionXX":
            # Explicitly marked as option
            options.append(param)
        elif not param.has_default:
            # No explicit hint, no default → argument
            arguments.append(param)
        elif param.concrete_type is bool:
            # Boolean parameters always become flags
            options.append(param)
        else:
            # Has default, non-boolean → Position-Based Hybrid
            # First param becomes optional argument, rest become options
            # (unless force_options is True)
            if force_options or arguments or options:
                # force_options enabled OR subsequent parameters → make them options
                options.append(param)
            else:
                # First parameter overall → make it an optional argument
                arguments.append(param)

    return arguments, options


def x_separate_arguments_and_options__mutmut_10(
    params: list[ParameterInfo],
    force_options: bool = False,
) -> tuple[list[ParameterInfo], list[ParameterInfo]]:
    """Separate parameters into arguments and options using Position-Based Hybrid.

    Rules:
    1. Explicit cli_hint='argument' → argument (even with default)
    2. Explicit cli_hint='option' → option (even without default)
    3. No hint + no default → argument
    4. No hint + has default + bool → option (flag)
    5. No hint + has default + non-bool → first becomes optional argument, rest become options
       (unless force_options=True, then all become options)

    Position-Based Hybrid provides natural UX:
    - First parameter feels like the "main thing" → optional positional argument
    - Additional parameters → explicit flags
    - Boolean parameters → always flags

    Example:
        def send(message: str = None, level: str = "INFO", verbose: bool = False):
            ...

        Becomes CLI:
            send [MESSAGE] --level INFO --verbose

        With force_options=True:
            send --message TEXT --level INFO --verbose

    Args:
        params: List of ParameterInfo objects
        force_options: If True, all parameters with defaults become options
                      (disables Position-Based Hybrid for first parameter)

    Returns:
        (arguments, options) tuple of parameter lists

    """
    arguments = []
    options = []

    for param in params:
        if param.cli_hint == "argument":
            # Explicitly marked as argument
            arguments.append(param)
        elif param.cli_hint == "OPTION":
            # Explicitly marked as option
            options.append(param)
        elif not param.has_default:
            # No explicit hint, no default → argument
            arguments.append(param)
        elif param.concrete_type is bool:
            # Boolean parameters always become flags
            options.append(param)
        else:
            # Has default, non-boolean → Position-Based Hybrid
            # First param becomes optional argument, rest become options
            # (unless force_options is True)
            if force_options or arguments or options:
                # force_options enabled OR subsequent parameters → make them options
                options.append(param)
            else:
                # First parameter overall → make it an optional argument
                arguments.append(param)

    return arguments, options


def x_separate_arguments_and_options__mutmut_11(
    params: list[ParameterInfo],
    force_options: bool = False,
) -> tuple[list[ParameterInfo], list[ParameterInfo]]:
    """Separate parameters into arguments and options using Position-Based Hybrid.

    Rules:
    1. Explicit cli_hint='argument' → argument (even with default)
    2. Explicit cli_hint='option' → option (even without default)
    3. No hint + no default → argument
    4. No hint + has default + bool → option (flag)
    5. No hint + has default + non-bool → first becomes optional argument, rest become options
       (unless force_options=True, then all become options)

    Position-Based Hybrid provides natural UX:
    - First parameter feels like the "main thing" → optional positional argument
    - Additional parameters → explicit flags
    - Boolean parameters → always flags

    Example:
        def send(message: str = None, level: str = "INFO", verbose: bool = False):
            ...

        Becomes CLI:
            send [MESSAGE] --level INFO --verbose

        With force_options=True:
            send --message TEXT --level INFO --verbose

    Args:
        params: List of ParameterInfo objects
        force_options: If True, all parameters with defaults become options
                      (disables Position-Based Hybrid for first parameter)

    Returns:
        (arguments, options) tuple of parameter lists

    """
    arguments = []
    options = []

    for param in params:
        if param.cli_hint == "argument":
            # Explicitly marked as argument
            arguments.append(param)
        elif param.cli_hint == "option":
            # Explicitly marked as option
            options.append(None)
        elif not param.has_default:
            # No explicit hint, no default → argument
            arguments.append(param)
        elif param.concrete_type is bool:
            # Boolean parameters always become flags
            options.append(param)
        else:
            # Has default, non-boolean → Position-Based Hybrid
            # First param becomes optional argument, rest become options
            # (unless force_options is True)
            if force_options or arguments or options:
                # force_options enabled OR subsequent parameters → make them options
                options.append(param)
            else:
                # First parameter overall → make it an optional argument
                arguments.append(param)

    return arguments, options


def x_separate_arguments_and_options__mutmut_12(
    params: list[ParameterInfo],
    force_options: bool = False,
) -> tuple[list[ParameterInfo], list[ParameterInfo]]:
    """Separate parameters into arguments and options using Position-Based Hybrid.

    Rules:
    1. Explicit cli_hint='argument' → argument (even with default)
    2. Explicit cli_hint='option' → option (even without default)
    3. No hint + no default → argument
    4. No hint + has default + bool → option (flag)
    5. No hint + has default + non-bool → first becomes optional argument, rest become options
       (unless force_options=True, then all become options)

    Position-Based Hybrid provides natural UX:
    - First parameter feels like the "main thing" → optional positional argument
    - Additional parameters → explicit flags
    - Boolean parameters → always flags

    Example:
        def send(message: str = None, level: str = "INFO", verbose: bool = False):
            ...

        Becomes CLI:
            send [MESSAGE] --level INFO --verbose

        With force_options=True:
            send --message TEXT --level INFO --verbose

    Args:
        params: List of ParameterInfo objects
        force_options: If True, all parameters with defaults become options
                      (disables Position-Based Hybrid for first parameter)

    Returns:
        (arguments, options) tuple of parameter lists

    """
    arguments = []
    options = []

    for param in params:
        if param.cli_hint == "argument":
            # Explicitly marked as argument
            arguments.append(param)
        elif param.cli_hint == "option":
            # Explicitly marked as option
            options.append(param)
        elif param.has_default:
            # No explicit hint, no default → argument
            arguments.append(param)
        elif param.concrete_type is bool:
            # Boolean parameters always become flags
            options.append(param)
        else:
            # Has default, non-boolean → Position-Based Hybrid
            # First param becomes optional argument, rest become options
            # (unless force_options is True)
            if force_options or arguments or options:
                # force_options enabled OR subsequent parameters → make them options
                options.append(param)
            else:
                # First parameter overall → make it an optional argument
                arguments.append(param)

    return arguments, options


def x_separate_arguments_and_options__mutmut_13(
    params: list[ParameterInfo],
    force_options: bool = False,
) -> tuple[list[ParameterInfo], list[ParameterInfo]]:
    """Separate parameters into arguments and options using Position-Based Hybrid.

    Rules:
    1. Explicit cli_hint='argument' → argument (even with default)
    2. Explicit cli_hint='option' → option (even without default)
    3. No hint + no default → argument
    4. No hint + has default + bool → option (flag)
    5. No hint + has default + non-bool → first becomes optional argument, rest become options
       (unless force_options=True, then all become options)

    Position-Based Hybrid provides natural UX:
    - First parameter feels like the "main thing" → optional positional argument
    - Additional parameters → explicit flags
    - Boolean parameters → always flags

    Example:
        def send(message: str = None, level: str = "INFO", verbose: bool = False):
            ...

        Becomes CLI:
            send [MESSAGE] --level INFO --verbose

        With force_options=True:
            send --message TEXT --level INFO --verbose

    Args:
        params: List of ParameterInfo objects
        force_options: If True, all parameters with defaults become options
                      (disables Position-Based Hybrid for first parameter)

    Returns:
        (arguments, options) tuple of parameter lists

    """
    arguments = []
    options = []

    for param in params:
        if param.cli_hint == "argument":
            # Explicitly marked as argument
            arguments.append(param)
        elif param.cli_hint == "option":
            # Explicitly marked as option
            options.append(param)
        elif not param.has_default:
            # No explicit hint, no default → argument
            arguments.append(None)
        elif param.concrete_type is bool:
            # Boolean parameters always become flags
            options.append(param)
        else:
            # Has default, non-boolean → Position-Based Hybrid
            # First param becomes optional argument, rest become options
            # (unless force_options is True)
            if force_options or arguments or options:
                # force_options enabled OR subsequent parameters → make them options
                options.append(param)
            else:
                # First parameter overall → make it an optional argument
                arguments.append(param)

    return arguments, options


def x_separate_arguments_and_options__mutmut_14(
    params: list[ParameterInfo],
    force_options: bool = False,
) -> tuple[list[ParameterInfo], list[ParameterInfo]]:
    """Separate parameters into arguments and options using Position-Based Hybrid.

    Rules:
    1. Explicit cli_hint='argument' → argument (even with default)
    2. Explicit cli_hint='option' → option (even without default)
    3. No hint + no default → argument
    4. No hint + has default + bool → option (flag)
    5. No hint + has default + non-bool → first becomes optional argument, rest become options
       (unless force_options=True, then all become options)

    Position-Based Hybrid provides natural UX:
    - First parameter feels like the "main thing" → optional positional argument
    - Additional parameters → explicit flags
    - Boolean parameters → always flags

    Example:
        def send(message: str = None, level: str = "INFO", verbose: bool = False):
            ...

        Becomes CLI:
            send [MESSAGE] --level INFO --verbose

        With force_options=True:
            send --message TEXT --level INFO --verbose

    Args:
        params: List of ParameterInfo objects
        force_options: If True, all parameters with defaults become options
                      (disables Position-Based Hybrid for first parameter)

    Returns:
        (arguments, options) tuple of parameter lists

    """
    arguments = []
    options = []

    for param in params:
        if param.cli_hint == "argument":
            # Explicitly marked as argument
            arguments.append(param)
        elif param.cli_hint == "option":
            # Explicitly marked as option
            options.append(param)
        elif not param.has_default:
            # No explicit hint, no default → argument
            arguments.append(param)
        elif param.concrete_type is not bool:
            # Boolean parameters always become flags
            options.append(param)
        else:
            # Has default, non-boolean → Position-Based Hybrid
            # First param becomes optional argument, rest become options
            # (unless force_options is True)
            if force_options or arguments or options:
                # force_options enabled OR subsequent parameters → make them options
                options.append(param)
            else:
                # First parameter overall → make it an optional argument
                arguments.append(param)

    return arguments, options


def x_separate_arguments_and_options__mutmut_15(
    params: list[ParameterInfo],
    force_options: bool = False,
) -> tuple[list[ParameterInfo], list[ParameterInfo]]:
    """Separate parameters into arguments and options using Position-Based Hybrid.

    Rules:
    1. Explicit cli_hint='argument' → argument (even with default)
    2. Explicit cli_hint='option' → option (even without default)
    3. No hint + no default → argument
    4. No hint + has default + bool → option (flag)
    5. No hint + has default + non-bool → first becomes optional argument, rest become options
       (unless force_options=True, then all become options)

    Position-Based Hybrid provides natural UX:
    - First parameter feels like the "main thing" → optional positional argument
    - Additional parameters → explicit flags
    - Boolean parameters → always flags

    Example:
        def send(message: str = None, level: str = "INFO", verbose: bool = False):
            ...

        Becomes CLI:
            send [MESSAGE] --level INFO --verbose

        With force_options=True:
            send --message TEXT --level INFO --verbose

    Args:
        params: List of ParameterInfo objects
        force_options: If True, all parameters with defaults become options
                      (disables Position-Based Hybrid for first parameter)

    Returns:
        (arguments, options) tuple of parameter lists

    """
    arguments = []
    options = []

    for param in params:
        if param.cli_hint == "argument":
            # Explicitly marked as argument
            arguments.append(param)
        elif param.cli_hint == "option":
            # Explicitly marked as option
            options.append(param)
        elif not param.has_default:
            # No explicit hint, no default → argument
            arguments.append(param)
        elif param.concrete_type is bool:
            # Boolean parameters always become flags
            options.append(None)
        else:
            # Has default, non-boolean → Position-Based Hybrid
            # First param becomes optional argument, rest become options
            # (unless force_options is True)
            if force_options or arguments or options:
                # force_options enabled OR subsequent parameters → make them options
                options.append(param)
            else:
                # First parameter overall → make it an optional argument
                arguments.append(param)

    return arguments, options


def x_separate_arguments_and_options__mutmut_16(
    params: list[ParameterInfo],
    force_options: bool = False,
) -> tuple[list[ParameterInfo], list[ParameterInfo]]:
    """Separate parameters into arguments and options using Position-Based Hybrid.

    Rules:
    1. Explicit cli_hint='argument' → argument (even with default)
    2. Explicit cli_hint='option' → option (even without default)
    3. No hint + no default → argument
    4. No hint + has default + bool → option (flag)
    5. No hint + has default + non-bool → first becomes optional argument, rest become options
       (unless force_options=True, then all become options)

    Position-Based Hybrid provides natural UX:
    - First parameter feels like the "main thing" → optional positional argument
    - Additional parameters → explicit flags
    - Boolean parameters → always flags

    Example:
        def send(message: str = None, level: str = "INFO", verbose: bool = False):
            ...

        Becomes CLI:
            send [MESSAGE] --level INFO --verbose

        With force_options=True:
            send --message TEXT --level INFO --verbose

    Args:
        params: List of ParameterInfo objects
        force_options: If True, all parameters with defaults become options
                      (disables Position-Based Hybrid for first parameter)

    Returns:
        (arguments, options) tuple of parameter lists

    """
    arguments = []
    options = []

    for param in params:
        if param.cli_hint == "argument":
            # Explicitly marked as argument
            arguments.append(param)
        elif param.cli_hint == "option":
            # Explicitly marked as option
            options.append(param)
        elif not param.has_default:
            # No explicit hint, no default → argument
            arguments.append(param)
        elif param.concrete_type is bool:
            # Boolean parameters always become flags
            options.append(param)
        else:
            # Has default, non-boolean → Position-Based Hybrid
            # First param becomes optional argument, rest become options
            # (unless force_options is True)
            if force_options or arguments and options:
                # force_options enabled OR subsequent parameters → make them options
                options.append(param)
            else:
                # First parameter overall → make it an optional argument
                arguments.append(param)

    return arguments, options


def x_separate_arguments_and_options__mutmut_17(
    params: list[ParameterInfo],
    force_options: bool = False,
) -> tuple[list[ParameterInfo], list[ParameterInfo]]:
    """Separate parameters into arguments and options using Position-Based Hybrid.

    Rules:
    1. Explicit cli_hint='argument' → argument (even with default)
    2. Explicit cli_hint='option' → option (even without default)
    3. No hint + no default → argument
    4. No hint + has default + bool → option (flag)
    5. No hint + has default + non-bool → first becomes optional argument, rest become options
       (unless force_options=True, then all become options)

    Position-Based Hybrid provides natural UX:
    - First parameter feels like the "main thing" → optional positional argument
    - Additional parameters → explicit flags
    - Boolean parameters → always flags

    Example:
        def send(message: str = None, level: str = "INFO", verbose: bool = False):
            ...

        Becomes CLI:
            send [MESSAGE] --level INFO --verbose

        With force_options=True:
            send --message TEXT --level INFO --verbose

    Args:
        params: List of ParameterInfo objects
        force_options: If True, all parameters with defaults become options
                      (disables Position-Based Hybrid for first parameter)

    Returns:
        (arguments, options) tuple of parameter lists

    """
    arguments = []
    options = []

    for param in params:
        if param.cli_hint == "argument":
            # Explicitly marked as argument
            arguments.append(param)
        elif param.cli_hint == "option":
            # Explicitly marked as option
            options.append(param)
        elif not param.has_default:
            # No explicit hint, no default → argument
            arguments.append(param)
        elif param.concrete_type is bool:
            # Boolean parameters always become flags
            options.append(param)
        else:
            # Has default, non-boolean → Position-Based Hybrid
            # First param becomes optional argument, rest become options
            # (unless force_options is True)
            if force_options and arguments or options:
                # force_options enabled OR subsequent parameters → make them options
                options.append(param)
            else:
                # First parameter overall → make it an optional argument
                arguments.append(param)

    return arguments, options


def x_separate_arguments_and_options__mutmut_18(
    params: list[ParameterInfo],
    force_options: bool = False,
) -> tuple[list[ParameterInfo], list[ParameterInfo]]:
    """Separate parameters into arguments and options using Position-Based Hybrid.

    Rules:
    1. Explicit cli_hint='argument' → argument (even with default)
    2. Explicit cli_hint='option' → option (even without default)
    3. No hint + no default → argument
    4. No hint + has default + bool → option (flag)
    5. No hint + has default + non-bool → first becomes optional argument, rest become options
       (unless force_options=True, then all become options)

    Position-Based Hybrid provides natural UX:
    - First parameter feels like the "main thing" → optional positional argument
    - Additional parameters → explicit flags
    - Boolean parameters → always flags

    Example:
        def send(message: str = None, level: str = "INFO", verbose: bool = False):
            ...

        Becomes CLI:
            send [MESSAGE] --level INFO --verbose

        With force_options=True:
            send --message TEXT --level INFO --verbose

    Args:
        params: List of ParameterInfo objects
        force_options: If True, all parameters with defaults become options
                      (disables Position-Based Hybrid for first parameter)

    Returns:
        (arguments, options) tuple of parameter lists

    """
    arguments = []
    options = []

    for param in params:
        if param.cli_hint == "argument":
            # Explicitly marked as argument
            arguments.append(param)
        elif param.cli_hint == "option":
            # Explicitly marked as option
            options.append(param)
        elif not param.has_default:
            # No explicit hint, no default → argument
            arguments.append(param)
        elif param.concrete_type is bool:
            # Boolean parameters always become flags
            options.append(param)
        else:
            # Has default, non-boolean → Position-Based Hybrid
            # First param becomes optional argument, rest become options
            # (unless force_options is True)
            if force_options or arguments or options:
                # force_options enabled OR subsequent parameters → make them options
                options.append(None)
            else:
                # First parameter overall → make it an optional argument
                arguments.append(param)

    return arguments, options


def x_separate_arguments_and_options__mutmut_19(
    params: list[ParameterInfo],
    force_options: bool = False,
) -> tuple[list[ParameterInfo], list[ParameterInfo]]:
    """Separate parameters into arguments and options using Position-Based Hybrid.

    Rules:
    1. Explicit cli_hint='argument' → argument (even with default)
    2. Explicit cli_hint='option' → option (even without default)
    3. No hint + no default → argument
    4. No hint + has default + bool → option (flag)
    5. No hint + has default + non-bool → first becomes optional argument, rest become options
       (unless force_options=True, then all become options)

    Position-Based Hybrid provides natural UX:
    - First parameter feels like the "main thing" → optional positional argument
    - Additional parameters → explicit flags
    - Boolean parameters → always flags

    Example:
        def send(message: str = None, level: str = "INFO", verbose: bool = False):
            ...

        Becomes CLI:
            send [MESSAGE] --level INFO --verbose

        With force_options=True:
            send --message TEXT --level INFO --verbose

    Args:
        params: List of ParameterInfo objects
        force_options: If True, all parameters with defaults become options
                      (disables Position-Based Hybrid for first parameter)

    Returns:
        (arguments, options) tuple of parameter lists

    """
    arguments = []
    options = []

    for param in params:
        if param.cli_hint == "argument":
            # Explicitly marked as argument
            arguments.append(param)
        elif param.cli_hint == "option":
            # Explicitly marked as option
            options.append(param)
        elif not param.has_default:
            # No explicit hint, no default → argument
            arguments.append(param)
        elif param.concrete_type is bool:
            # Boolean parameters always become flags
            options.append(param)
        else:
            # Has default, non-boolean → Position-Based Hybrid
            # First param becomes optional argument, rest become options
            # (unless force_options is True)
            if force_options or arguments or options:
                # force_options enabled OR subsequent parameters → make them options
                options.append(param)
            else:
                # First parameter overall → make it an optional argument
                arguments.append(None)

    return arguments, options


x_separate_arguments_and_options__mutmut_mutants: ClassVar[MutantDict] = {
    "x_separate_arguments_and_options__mutmut_1": x_separate_arguments_and_options__mutmut_1,
    "x_separate_arguments_and_options__mutmut_2": x_separate_arguments_and_options__mutmut_2,
    "x_separate_arguments_and_options__mutmut_3": x_separate_arguments_and_options__mutmut_3,
    "x_separate_arguments_and_options__mutmut_4": x_separate_arguments_and_options__mutmut_4,
    "x_separate_arguments_and_options__mutmut_5": x_separate_arguments_and_options__mutmut_5,
    "x_separate_arguments_and_options__mutmut_6": x_separate_arguments_and_options__mutmut_6,
    "x_separate_arguments_and_options__mutmut_7": x_separate_arguments_and_options__mutmut_7,
    "x_separate_arguments_and_options__mutmut_8": x_separate_arguments_and_options__mutmut_8,
    "x_separate_arguments_and_options__mutmut_9": x_separate_arguments_and_options__mutmut_9,
    "x_separate_arguments_and_options__mutmut_10": x_separate_arguments_and_options__mutmut_10,
    "x_separate_arguments_and_options__mutmut_11": x_separate_arguments_and_options__mutmut_11,
    "x_separate_arguments_and_options__mutmut_12": x_separate_arguments_and_options__mutmut_12,
    "x_separate_arguments_and_options__mutmut_13": x_separate_arguments_and_options__mutmut_13,
    "x_separate_arguments_and_options__mutmut_14": x_separate_arguments_and_options__mutmut_14,
    "x_separate_arguments_and_options__mutmut_15": x_separate_arguments_and_options__mutmut_15,
    "x_separate_arguments_and_options__mutmut_16": x_separate_arguments_and_options__mutmut_16,
    "x_separate_arguments_and_options__mutmut_17": x_separate_arguments_and_options__mutmut_17,
    "x_separate_arguments_and_options__mutmut_18": x_separate_arguments_and_options__mutmut_18,
    "x_separate_arguments_and_options__mutmut_19": x_separate_arguments_and_options__mutmut_19,
}


def separate_arguments_and_options(*args, **kwargs):
    result = _mutmut_trampoline(
        x_separate_arguments_and_options__mutmut_orig,
        x_separate_arguments_and_options__mutmut_mutants,
        args,
        kwargs,
    )
    return result


separate_arguments_and_options.__signature__ = _mutmut_signature(x_separate_arguments_and_options__mutmut_orig)
x_separate_arguments_and_options__mutmut_orig.__name__ = "x_separate_arguments_and_options"


def x_apply_click_option__mutmut_orig(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_1(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = None

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_2(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace(None, '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_3(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', None)}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_4(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_5(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_6(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('XX_XX', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_7(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', 'XX-XX')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_8(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = None

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_9(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" or not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_10(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint != "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_11(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "XXoptionXX" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_12(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "OPTION" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_13(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_14(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is not bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_15(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(None)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_16(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            None,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_17(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=None,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_18(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_19(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=None,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_20(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=None,
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_21(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_22(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_23(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_24(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_25(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_26(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=False,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_27(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(None)


def x_apply_click_option__mutmut_28(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        None,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_29(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=None,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_30(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_31(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=None,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_32(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=None,
    )(func)


def x_apply_click_option__mutmut_33(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_34(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        default=param.default if param.has_default else None,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_35(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        required=is_required,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_36(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        help=f"{param.name} option",
    )(func)


def x_apply_click_option__mutmut_37(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click option decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    option_name = f"--{param.name.replace('_', '-')}"

    # Determine if this is a required option (explicit hint='option' without default)
    is_required = param.cli_hint == "option" and not param.has_default

    # Handle boolean flags
    if param.concrete_type is bool:
        return click.option(
            option_name,
            is_flag=True,
            default=param.default if param.has_default else None,
            required=is_required,
            help=f"{param.name} flag",
        )(func)

    # Handle regular options
    return click.option(
        option_name,
        type=param.concrete_type,
        default=param.default if param.has_default else None,
        required=is_required,
    )(func)


x_apply_click_option__mutmut_mutants: ClassVar[MutantDict] = {
    "x_apply_click_option__mutmut_1": x_apply_click_option__mutmut_1,
    "x_apply_click_option__mutmut_2": x_apply_click_option__mutmut_2,
    "x_apply_click_option__mutmut_3": x_apply_click_option__mutmut_3,
    "x_apply_click_option__mutmut_4": x_apply_click_option__mutmut_4,
    "x_apply_click_option__mutmut_5": x_apply_click_option__mutmut_5,
    "x_apply_click_option__mutmut_6": x_apply_click_option__mutmut_6,
    "x_apply_click_option__mutmut_7": x_apply_click_option__mutmut_7,
    "x_apply_click_option__mutmut_8": x_apply_click_option__mutmut_8,
    "x_apply_click_option__mutmut_9": x_apply_click_option__mutmut_9,
    "x_apply_click_option__mutmut_10": x_apply_click_option__mutmut_10,
    "x_apply_click_option__mutmut_11": x_apply_click_option__mutmut_11,
    "x_apply_click_option__mutmut_12": x_apply_click_option__mutmut_12,
    "x_apply_click_option__mutmut_13": x_apply_click_option__mutmut_13,
    "x_apply_click_option__mutmut_14": x_apply_click_option__mutmut_14,
    "x_apply_click_option__mutmut_15": x_apply_click_option__mutmut_15,
    "x_apply_click_option__mutmut_16": x_apply_click_option__mutmut_16,
    "x_apply_click_option__mutmut_17": x_apply_click_option__mutmut_17,
    "x_apply_click_option__mutmut_18": x_apply_click_option__mutmut_18,
    "x_apply_click_option__mutmut_19": x_apply_click_option__mutmut_19,
    "x_apply_click_option__mutmut_20": x_apply_click_option__mutmut_20,
    "x_apply_click_option__mutmut_21": x_apply_click_option__mutmut_21,
    "x_apply_click_option__mutmut_22": x_apply_click_option__mutmut_22,
    "x_apply_click_option__mutmut_23": x_apply_click_option__mutmut_23,
    "x_apply_click_option__mutmut_24": x_apply_click_option__mutmut_24,
    "x_apply_click_option__mutmut_25": x_apply_click_option__mutmut_25,
    "x_apply_click_option__mutmut_26": x_apply_click_option__mutmut_26,
    "x_apply_click_option__mutmut_27": x_apply_click_option__mutmut_27,
    "x_apply_click_option__mutmut_28": x_apply_click_option__mutmut_28,
    "x_apply_click_option__mutmut_29": x_apply_click_option__mutmut_29,
    "x_apply_click_option__mutmut_30": x_apply_click_option__mutmut_30,
    "x_apply_click_option__mutmut_31": x_apply_click_option__mutmut_31,
    "x_apply_click_option__mutmut_32": x_apply_click_option__mutmut_32,
    "x_apply_click_option__mutmut_33": x_apply_click_option__mutmut_33,
    "x_apply_click_option__mutmut_34": x_apply_click_option__mutmut_34,
    "x_apply_click_option__mutmut_35": x_apply_click_option__mutmut_35,
    "x_apply_click_option__mutmut_36": x_apply_click_option__mutmut_36,
    "x_apply_click_option__mutmut_37": x_apply_click_option__mutmut_37,
}


def apply_click_option(*args, **kwargs):
    result = _mutmut_trampoline(
        x_apply_click_option__mutmut_orig, x_apply_click_option__mutmut_mutants, args, kwargs
    )
    return result


apply_click_option.__signature__ = _mutmut_signature(x_apply_click_option__mutmut_orig)
x_apply_click_option__mutmut_orig.__name__ = "x_apply_click_option"


def x_apply_click_argument__mutmut_orig(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click argument decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    # Arguments can have defaults (makes them optional in Click)
    if param.has_default:
        return click.argument(
            param.name,
            type=param.concrete_type,
            default=param.default,
        )(func)
    else:
        return click.argument(
            param.name,
            type=param.concrete_type,
        )(func)


def x_apply_click_argument__mutmut_1(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click argument decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    # Arguments can have defaults (makes them optional in Click)
    if param.has_default:
        return click.argument(
            param.name,
            type=param.concrete_type,
            default=param.default,
        )(None)
    else:
        return click.argument(
            param.name,
            type=param.concrete_type,
        )(func)


def x_apply_click_argument__mutmut_2(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click argument decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    # Arguments can have defaults (makes them optional in Click)
    if param.has_default:
        return click.argument(
            None,
            type=param.concrete_type,
            default=param.default,
        )(func)
    else:
        return click.argument(
            param.name,
            type=param.concrete_type,
        )(func)


def x_apply_click_argument__mutmut_3(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click argument decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    # Arguments can have defaults (makes them optional in Click)
    if param.has_default:
        return click.argument(
            param.name,
            type=None,
            default=param.default,
        )(func)
    else:
        return click.argument(
            param.name,
            type=param.concrete_type,
        )(func)


def x_apply_click_argument__mutmut_4(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click argument decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    # Arguments can have defaults (makes them optional in Click)
    if param.has_default:
        return click.argument(
            param.name,
            type=param.concrete_type,
            default=None,
        )(func)
    else:
        return click.argument(
            param.name,
            type=param.concrete_type,
        )(func)


def x_apply_click_argument__mutmut_5(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click argument decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    # Arguments can have defaults (makes them optional in Click)
    if param.has_default:
        return click.argument(
            type=param.concrete_type,
            default=param.default,
        )(func)
    else:
        return click.argument(
            param.name,
            type=param.concrete_type,
        )(func)


def x_apply_click_argument__mutmut_6(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click argument decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    # Arguments can have defaults (makes them optional in Click)
    if param.has_default:
        return click.argument(
            param.name,
            default=param.default,
        )(func)
    else:
        return click.argument(
            param.name,
            type=param.concrete_type,
        )(func)


def x_apply_click_argument__mutmut_7(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click argument decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    # Arguments can have defaults (makes them optional in Click)
    if param.has_default:
        return click.argument(
            param.name,
            type=param.concrete_type,
        )(func)
    else:
        return click.argument(
            param.name,
            type=param.concrete_type,
        )(func)


def x_apply_click_argument__mutmut_8(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click argument decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    # Arguments can have defaults (makes them optional in Click)
    if param.has_default:
        return click.argument(
            param.name,
            type=param.concrete_type,
            default=param.default,
        )(func)
    else:
        return click.argument(
            param.name,
            type=param.concrete_type,
        )(None)


def x_apply_click_argument__mutmut_9(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click argument decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    # Arguments can have defaults (makes them optional in Click)
    if param.has_default:
        return click.argument(
            param.name,
            type=param.concrete_type,
            default=param.default,
        )(func)
    else:
        return click.argument(
            None,
            type=param.concrete_type,
        )(func)


def x_apply_click_argument__mutmut_10(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click argument decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    # Arguments can have defaults (makes them optional in Click)
    if param.has_default:
        return click.argument(
            param.name,
            type=param.concrete_type,
            default=param.default,
        )(func)
    else:
        return click.argument(
            param.name,
            type=None,
        )(func)


def x_apply_click_argument__mutmut_11(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click argument decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    # Arguments can have defaults (makes them optional in Click)
    if param.has_default:
        return click.argument(
            param.name,
            type=param.concrete_type,
            default=param.default,
        )(func)
    else:
        return click.argument(
            type=param.concrete_type,
        )(func)


def x_apply_click_argument__mutmut_12(func: Any, param: ParameterInfo) -> Any:
    """Apply a Click argument decorator to a function.

    Args:
        func: Function to decorate
        param: Parameter information

    Returns:
        Decorated function

    """
    # Arguments can have defaults (makes them optional in Click)
    if param.has_default:
        return click.argument(
            param.name,
            type=param.concrete_type,
            default=param.default,
        )(func)
    else:
        return click.argument(
            param.name,
        )(func)


x_apply_click_argument__mutmut_mutants: ClassVar[MutantDict] = {
    "x_apply_click_argument__mutmut_1": x_apply_click_argument__mutmut_1,
    "x_apply_click_argument__mutmut_2": x_apply_click_argument__mutmut_2,
    "x_apply_click_argument__mutmut_3": x_apply_click_argument__mutmut_3,
    "x_apply_click_argument__mutmut_4": x_apply_click_argument__mutmut_4,
    "x_apply_click_argument__mutmut_5": x_apply_click_argument__mutmut_5,
    "x_apply_click_argument__mutmut_6": x_apply_click_argument__mutmut_6,
    "x_apply_click_argument__mutmut_7": x_apply_click_argument__mutmut_7,
    "x_apply_click_argument__mutmut_8": x_apply_click_argument__mutmut_8,
    "x_apply_click_argument__mutmut_9": x_apply_click_argument__mutmut_9,
    "x_apply_click_argument__mutmut_10": x_apply_click_argument__mutmut_10,
    "x_apply_click_argument__mutmut_11": x_apply_click_argument__mutmut_11,
    "x_apply_click_argument__mutmut_12": x_apply_click_argument__mutmut_12,
}


def apply_click_argument(*args, **kwargs):
    result = _mutmut_trampoline(
        x_apply_click_argument__mutmut_orig, x_apply_click_argument__mutmut_mutants, args, kwargs
    )
    return result


apply_click_argument.__signature__ = _mutmut_signature(x_apply_click_argument__mutmut_orig)
x_apply_click_argument__mutmut_orig.__name__ = "x_apply_click_argument"


# <3 🧱🤝💻🪄
