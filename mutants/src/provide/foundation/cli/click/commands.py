# provide/foundation/cli/click/commands.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Click command building and integration.

Builds individual Click commands from CommandInfo objects and integrates
them with Click groups.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from provide.foundation.cli.click.parameters import (
    apply_click_argument,
    apply_click_option,
    separate_arguments_and_options,
)
from provide.foundation.cli.deps import click
from provide.foundation.cli.errors import CLIBuildError
from provide.foundation.hub.introspection import introspect_parameters

if TYPE_CHECKING:
    from click import Command, Group

    from provide.foundation.hub.info import CommandInfo
    from provide.foundation.hub.registry import Registry

__all__ = [
    "add_command_to_group",
    "build_click_command_from_info",
]
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


def x_build_click_command_from_info__mutmut_orig(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_1(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = None

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_2(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(None) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_3(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is not None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_4(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = None

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_5(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get(None, False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_6(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", None)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_7(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get(False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_8(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", )

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_9(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("XXforce_optionsXX", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_10(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("FORCE_OPTIONS", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_11(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", True)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_12(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = None

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_13(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(None, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_14(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=None)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_15(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_16(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, )

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_17(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = None

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_18(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(None):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_19(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = None

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_20(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(None, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_21(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, None)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_22(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_23(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, )

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_24(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(None):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_25(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = None

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_26(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(None, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_27(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, None)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_28(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_29(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, )

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_30(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = None

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_31(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=None,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_32(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=None,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_33(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=None,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_34(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=None,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_35(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_36(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_37(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_38(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_39(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(None, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_40(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, None):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_41(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr("__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_42(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, ):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_43(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "XX__click_params__XX"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_44(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__CLICK_PARAMS__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_45(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = None

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_46(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(None)

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_47(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(None))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_48(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = None

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_49(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            None,
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_50(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=None,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_51(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            cause=None,
        ) from e


def x_build_click_command_from_info__mutmut_52(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            command_name=info.name,
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_53(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            cause=e,
        ) from e


def x_build_click_command_from_info__mutmut_54(info: CommandInfo) -> Command:
    """Build a Click command directly from CommandInfo.

    This is a pure builder function that creates a Click command from
    a CommandInfo object without requiring registry access. Supports
    typing.Annotated for explicit argument/option control.

    Args:
        info: CommandInfo object with command metadata

    Returns:
        Click Command object

    Raises:
        CLIBuildError: If command building fails

    Example:
        >>> from provide.foundation.hub.info import CommandInfo
        >>> info = CommandInfo(name="greet", func=greet_func, description="Greet someone")
        >>> click_cmd = build_click_command_from_info(info)
        >>> isinstance(click_cmd, click.Command)
        True

    """
    try:
        # Introspect parameters if not already done
        params = introspect_parameters(info.func) if info.parameters is None else info.parameters

        # Check if command wants to force all defaults to be options
        force_options = info.metadata.get("force_options", False)

        # Separate into arguments and options
        arguments, options = separate_arguments_and_options(params, force_options=force_options)

        # Create a wrapper to avoid modifying the original function
        # Click decorators modify functions in-place, so we need to protect info.func
        import functools

        @functools.wraps(info.func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return info.func(*args, **kwargs)

        # Start with the wrapper function
        decorated_func = wrapper

        # Process options in reverse order (for decorator stacking)
        for param in reversed(options):
            decorated_func = apply_click_option(decorated_func, param)

        # Process arguments in reverse order
        for param in reversed(arguments):
            decorated_func = apply_click_argument(decorated_func, param)

        # Create the Click command with the decorated function
        cmd = click.Command(
            name=info.name,
            callback=decorated_func,
            help=info.description,
            hidden=info.hidden,
        )

        # Copy over the params from the decorated function
        if hasattr(decorated_func, "__click_params__"):
            cmd.params = list(reversed(decorated_func.__click_params__))

        # Restore the original function as the callback
        # The wrapper was only needed to collect parameters without modifying info.func
        cmd.callback = info.func

        return cmd

    except Exception as e:
        raise CLIBuildError(
            f"Failed to build Click command '{info.name}': {e}",
            command_name=info.name,
            ) from e

x_build_click_command_from_info__mutmut_mutants : ClassVar[MutantDict] = {
'x_build_click_command_from_info__mutmut_1': x_build_click_command_from_info__mutmut_1, 
    'x_build_click_command_from_info__mutmut_2': x_build_click_command_from_info__mutmut_2, 
    'x_build_click_command_from_info__mutmut_3': x_build_click_command_from_info__mutmut_3, 
    'x_build_click_command_from_info__mutmut_4': x_build_click_command_from_info__mutmut_4, 
    'x_build_click_command_from_info__mutmut_5': x_build_click_command_from_info__mutmut_5, 
    'x_build_click_command_from_info__mutmut_6': x_build_click_command_from_info__mutmut_6, 
    'x_build_click_command_from_info__mutmut_7': x_build_click_command_from_info__mutmut_7, 
    'x_build_click_command_from_info__mutmut_8': x_build_click_command_from_info__mutmut_8, 
    'x_build_click_command_from_info__mutmut_9': x_build_click_command_from_info__mutmut_9, 
    'x_build_click_command_from_info__mutmut_10': x_build_click_command_from_info__mutmut_10, 
    'x_build_click_command_from_info__mutmut_11': x_build_click_command_from_info__mutmut_11, 
    'x_build_click_command_from_info__mutmut_12': x_build_click_command_from_info__mutmut_12, 
    'x_build_click_command_from_info__mutmut_13': x_build_click_command_from_info__mutmut_13, 
    'x_build_click_command_from_info__mutmut_14': x_build_click_command_from_info__mutmut_14, 
    'x_build_click_command_from_info__mutmut_15': x_build_click_command_from_info__mutmut_15, 
    'x_build_click_command_from_info__mutmut_16': x_build_click_command_from_info__mutmut_16, 
    'x_build_click_command_from_info__mutmut_17': x_build_click_command_from_info__mutmut_17, 
    'x_build_click_command_from_info__mutmut_18': x_build_click_command_from_info__mutmut_18, 
    'x_build_click_command_from_info__mutmut_19': x_build_click_command_from_info__mutmut_19, 
    'x_build_click_command_from_info__mutmut_20': x_build_click_command_from_info__mutmut_20, 
    'x_build_click_command_from_info__mutmut_21': x_build_click_command_from_info__mutmut_21, 
    'x_build_click_command_from_info__mutmut_22': x_build_click_command_from_info__mutmut_22, 
    'x_build_click_command_from_info__mutmut_23': x_build_click_command_from_info__mutmut_23, 
    'x_build_click_command_from_info__mutmut_24': x_build_click_command_from_info__mutmut_24, 
    'x_build_click_command_from_info__mutmut_25': x_build_click_command_from_info__mutmut_25, 
    'x_build_click_command_from_info__mutmut_26': x_build_click_command_from_info__mutmut_26, 
    'x_build_click_command_from_info__mutmut_27': x_build_click_command_from_info__mutmut_27, 
    'x_build_click_command_from_info__mutmut_28': x_build_click_command_from_info__mutmut_28, 
    'x_build_click_command_from_info__mutmut_29': x_build_click_command_from_info__mutmut_29, 
    'x_build_click_command_from_info__mutmut_30': x_build_click_command_from_info__mutmut_30, 
    'x_build_click_command_from_info__mutmut_31': x_build_click_command_from_info__mutmut_31, 
    'x_build_click_command_from_info__mutmut_32': x_build_click_command_from_info__mutmut_32, 
    'x_build_click_command_from_info__mutmut_33': x_build_click_command_from_info__mutmut_33, 
    'x_build_click_command_from_info__mutmut_34': x_build_click_command_from_info__mutmut_34, 
    'x_build_click_command_from_info__mutmut_35': x_build_click_command_from_info__mutmut_35, 
    'x_build_click_command_from_info__mutmut_36': x_build_click_command_from_info__mutmut_36, 
    'x_build_click_command_from_info__mutmut_37': x_build_click_command_from_info__mutmut_37, 
    'x_build_click_command_from_info__mutmut_38': x_build_click_command_from_info__mutmut_38, 
    'x_build_click_command_from_info__mutmut_39': x_build_click_command_from_info__mutmut_39, 
    'x_build_click_command_from_info__mutmut_40': x_build_click_command_from_info__mutmut_40, 
    'x_build_click_command_from_info__mutmut_41': x_build_click_command_from_info__mutmut_41, 
    'x_build_click_command_from_info__mutmut_42': x_build_click_command_from_info__mutmut_42, 
    'x_build_click_command_from_info__mutmut_43': x_build_click_command_from_info__mutmut_43, 
    'x_build_click_command_from_info__mutmut_44': x_build_click_command_from_info__mutmut_44, 
    'x_build_click_command_from_info__mutmut_45': x_build_click_command_from_info__mutmut_45, 
    'x_build_click_command_from_info__mutmut_46': x_build_click_command_from_info__mutmut_46, 
    'x_build_click_command_from_info__mutmut_47': x_build_click_command_from_info__mutmut_47, 
    'x_build_click_command_from_info__mutmut_48': x_build_click_command_from_info__mutmut_48, 
    'x_build_click_command_from_info__mutmut_49': x_build_click_command_from_info__mutmut_49, 
    'x_build_click_command_from_info__mutmut_50': x_build_click_command_from_info__mutmut_50, 
    'x_build_click_command_from_info__mutmut_51': x_build_click_command_from_info__mutmut_51, 
    'x_build_click_command_from_info__mutmut_52': x_build_click_command_from_info__mutmut_52, 
    'x_build_click_command_from_info__mutmut_53': x_build_click_command_from_info__mutmut_53, 
    'x_build_click_command_from_info__mutmut_54': x_build_click_command_from_info__mutmut_54
}

def build_click_command_from_info(*args, **kwargs):
    result = _mutmut_trampoline(x_build_click_command_from_info__mutmut_orig, x_build_click_command_from_info__mutmut_mutants, args, kwargs)
    return result 

build_click_command_from_info.__signature__ = _mutmut_signature(x_build_click_command_from_info__mutmut_orig)
x_build_click_command_from_info__mutmut_orig.__name__ = 'x_build_click_command_from_info'


def x_add_command_to_group__mutmut_orig(
    info: CommandInfo,
    groups: dict[str, Group],
    root_group: Group,
    registry: Registry,
) -> None:
    """Build and add a Click command to the appropriate group.

    Args:
        info: CommandInfo object for the command
        groups: Dictionary of existing groups
        root_group: Root group
        registry: Command registry (unused, kept for signature compatibility during refactor)

    """
    click_cmd = build_click_command_from_info(info)
    if not click_cmd:
        return

    # Add to parent group or root
    if info.parent and info.parent in groups:
        groups[info.parent].add_command(click_cmd)
    else:
        # Parent not found or no parent, add to root
        root_group.add_command(click_cmd)


def x_add_command_to_group__mutmut_1(
    info: CommandInfo,
    groups: dict[str, Group],
    root_group: Group,
    registry: Registry,
) -> None:
    """Build and add a Click command to the appropriate group.

    Args:
        info: CommandInfo object for the command
        groups: Dictionary of existing groups
        root_group: Root group
        registry: Command registry (unused, kept for signature compatibility during refactor)

    """
    click_cmd = None
    if not click_cmd:
        return

    # Add to parent group or root
    if info.parent and info.parent in groups:
        groups[info.parent].add_command(click_cmd)
    else:
        # Parent not found or no parent, add to root
        root_group.add_command(click_cmd)


def x_add_command_to_group__mutmut_2(
    info: CommandInfo,
    groups: dict[str, Group],
    root_group: Group,
    registry: Registry,
) -> None:
    """Build and add a Click command to the appropriate group.

    Args:
        info: CommandInfo object for the command
        groups: Dictionary of existing groups
        root_group: Root group
        registry: Command registry (unused, kept for signature compatibility during refactor)

    """
    click_cmd = build_click_command_from_info(None)
    if not click_cmd:
        return

    # Add to parent group or root
    if info.parent and info.parent in groups:
        groups[info.parent].add_command(click_cmd)
    else:
        # Parent not found or no parent, add to root
        root_group.add_command(click_cmd)


def x_add_command_to_group__mutmut_3(
    info: CommandInfo,
    groups: dict[str, Group],
    root_group: Group,
    registry: Registry,
) -> None:
    """Build and add a Click command to the appropriate group.

    Args:
        info: CommandInfo object for the command
        groups: Dictionary of existing groups
        root_group: Root group
        registry: Command registry (unused, kept for signature compatibility during refactor)

    """
    click_cmd = build_click_command_from_info(info)
    if click_cmd:
        return

    # Add to parent group or root
    if info.parent and info.parent in groups:
        groups[info.parent].add_command(click_cmd)
    else:
        # Parent not found or no parent, add to root
        root_group.add_command(click_cmd)


def x_add_command_to_group__mutmut_4(
    info: CommandInfo,
    groups: dict[str, Group],
    root_group: Group,
    registry: Registry,
) -> None:
    """Build and add a Click command to the appropriate group.

    Args:
        info: CommandInfo object for the command
        groups: Dictionary of existing groups
        root_group: Root group
        registry: Command registry (unused, kept for signature compatibility during refactor)

    """
    click_cmd = build_click_command_from_info(info)
    if not click_cmd:
        return

    # Add to parent group or root
    if info.parent or info.parent in groups:
        groups[info.parent].add_command(click_cmd)
    else:
        # Parent not found or no parent, add to root
        root_group.add_command(click_cmd)


def x_add_command_to_group__mutmut_5(
    info: CommandInfo,
    groups: dict[str, Group],
    root_group: Group,
    registry: Registry,
) -> None:
    """Build and add a Click command to the appropriate group.

    Args:
        info: CommandInfo object for the command
        groups: Dictionary of existing groups
        root_group: Root group
        registry: Command registry (unused, kept for signature compatibility during refactor)

    """
    click_cmd = build_click_command_from_info(info)
    if not click_cmd:
        return

    # Add to parent group or root
    if info.parent and info.parent not in groups:
        groups[info.parent].add_command(click_cmd)
    else:
        # Parent not found or no parent, add to root
        root_group.add_command(click_cmd)


def x_add_command_to_group__mutmut_6(
    info: CommandInfo,
    groups: dict[str, Group],
    root_group: Group,
    registry: Registry,
) -> None:
    """Build and add a Click command to the appropriate group.

    Args:
        info: CommandInfo object for the command
        groups: Dictionary of existing groups
        root_group: Root group
        registry: Command registry (unused, kept for signature compatibility during refactor)

    """
    click_cmd = build_click_command_from_info(info)
    if not click_cmd:
        return

    # Add to parent group or root
    if info.parent and info.parent in groups:
        groups[info.parent].add_command(None)
    else:
        # Parent not found or no parent, add to root
        root_group.add_command(click_cmd)


def x_add_command_to_group__mutmut_7(
    info: CommandInfo,
    groups: dict[str, Group],
    root_group: Group,
    registry: Registry,
) -> None:
    """Build and add a Click command to the appropriate group.

    Args:
        info: CommandInfo object for the command
        groups: Dictionary of existing groups
        root_group: Root group
        registry: Command registry (unused, kept for signature compatibility during refactor)

    """
    click_cmd = build_click_command_from_info(info)
    if not click_cmd:
        return

    # Add to parent group or root
    if info.parent and info.parent in groups:
        groups[info.parent].add_command(click_cmd)
    else:
        # Parent not found or no parent, add to root
        root_group.add_command(None)

x_add_command_to_group__mutmut_mutants : ClassVar[MutantDict] = {
'x_add_command_to_group__mutmut_1': x_add_command_to_group__mutmut_1, 
    'x_add_command_to_group__mutmut_2': x_add_command_to_group__mutmut_2, 
    'x_add_command_to_group__mutmut_3': x_add_command_to_group__mutmut_3, 
    'x_add_command_to_group__mutmut_4': x_add_command_to_group__mutmut_4, 
    'x_add_command_to_group__mutmut_5': x_add_command_to_group__mutmut_5, 
    'x_add_command_to_group__mutmut_6': x_add_command_to_group__mutmut_6, 
    'x_add_command_to_group__mutmut_7': x_add_command_to_group__mutmut_7
}

def add_command_to_group(*args, **kwargs):
    result = _mutmut_trampoline(x_add_command_to_group__mutmut_orig, x_add_command_to_group__mutmut_mutants, args, kwargs)
    return result 

add_command_to_group.__signature__ = _mutmut_signature(x_add_command_to_group__mutmut_orig)
x_add_command_to_group__mutmut_orig.__name__ = 'x_add_command_to_group'


# <3 🧱🤝💻🪄
