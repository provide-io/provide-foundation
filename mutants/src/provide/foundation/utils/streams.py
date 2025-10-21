# provide/foundation/utils/streams.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import io
import sys
from typing import TextIO

"""Stream utilities for foundation library."""
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


def x_get_safe_stderr__mutmut_orig() -> TextIO:
    """Get a safe stderr stream, falling back to StringIO if stderr is not available.

    This is used during initialization when sys.stderr might not be available
    (e.g., in some embedded Python environments or during testing).

    Returns:
        A writable text stream, either sys.stderr or io.StringIO()

    """
    # Check if stderr exists, is not None, and is not closed
    if (
        hasattr(sys, "stderr")
        and sys.stderr is not None
        and not (hasattr(sys.stderr, "closed") and sys.stderr.closed)
    ):
        return sys.stderr
    else:
        return io.StringIO()


def x_get_safe_stderr__mutmut_1() -> TextIO:
    """Get a safe stderr stream, falling back to StringIO if stderr is not available.

    This is used during initialization when sys.stderr might not be available
    (e.g., in some embedded Python environments or during testing).

    Returns:
        A writable text stream, either sys.stderr or io.StringIO()

    """
    # Check if stderr exists, is not None, and is not closed
    if (
        hasattr(sys, "stderr")
        and sys.stderr is not None or not (hasattr(sys.stderr, "closed") and sys.stderr.closed)
    ):
        return sys.stderr
    else:
        return io.StringIO()


def x_get_safe_stderr__mutmut_2() -> TextIO:
    """Get a safe stderr stream, falling back to StringIO if stderr is not available.

    This is used during initialization when sys.stderr might not be available
    (e.g., in some embedded Python environments or during testing).

    Returns:
        A writable text stream, either sys.stderr or io.StringIO()

    """
    # Check if stderr exists, is not None, and is not closed
    if (
        hasattr(sys, "stderr") or sys.stderr is not None
        and not (hasattr(sys.stderr, "closed") and sys.stderr.closed)
    ):
        return sys.stderr
    else:
        return io.StringIO()


def x_get_safe_stderr__mutmut_3() -> TextIO:
    """Get a safe stderr stream, falling back to StringIO if stderr is not available.

    This is used during initialization when sys.stderr might not be available
    (e.g., in some embedded Python environments or during testing).

    Returns:
        A writable text stream, either sys.stderr or io.StringIO()

    """
    # Check if stderr exists, is not None, and is not closed
    if (
        hasattr(None, "stderr")
        and sys.stderr is not None
        and not (hasattr(sys.stderr, "closed") and sys.stderr.closed)
    ):
        return sys.stderr
    else:
        return io.StringIO()


def x_get_safe_stderr__mutmut_4() -> TextIO:
    """Get a safe stderr stream, falling back to StringIO if stderr is not available.

    This is used during initialization when sys.stderr might not be available
    (e.g., in some embedded Python environments or during testing).

    Returns:
        A writable text stream, either sys.stderr or io.StringIO()

    """
    # Check if stderr exists, is not None, and is not closed
    if (
        hasattr(sys, None)
        and sys.stderr is not None
        and not (hasattr(sys.stderr, "closed") and sys.stderr.closed)
    ):
        return sys.stderr
    else:
        return io.StringIO()


def x_get_safe_stderr__mutmut_5() -> TextIO:
    """Get a safe stderr stream, falling back to StringIO if stderr is not available.

    This is used during initialization when sys.stderr might not be available
    (e.g., in some embedded Python environments or during testing).

    Returns:
        A writable text stream, either sys.stderr or io.StringIO()

    """
    # Check if stderr exists, is not None, and is not closed
    if (
        hasattr("stderr")
        and sys.stderr is not None
        and not (hasattr(sys.stderr, "closed") and sys.stderr.closed)
    ):
        return sys.stderr
    else:
        return io.StringIO()


def x_get_safe_stderr__mutmut_6() -> TextIO:
    """Get a safe stderr stream, falling back to StringIO if stderr is not available.

    This is used during initialization when sys.stderr might not be available
    (e.g., in some embedded Python environments or during testing).

    Returns:
        A writable text stream, either sys.stderr or io.StringIO()

    """
    # Check if stderr exists, is not None, and is not closed
    if (
        hasattr(sys, )
        and sys.stderr is not None
        and not (hasattr(sys.stderr, "closed") and sys.stderr.closed)
    ):
        return sys.stderr
    else:
        return io.StringIO()


def x_get_safe_stderr__mutmut_7() -> TextIO:
    """Get a safe stderr stream, falling back to StringIO if stderr is not available.

    This is used during initialization when sys.stderr might not be available
    (e.g., in some embedded Python environments or during testing).

    Returns:
        A writable text stream, either sys.stderr or io.StringIO()

    """
    # Check if stderr exists, is not None, and is not closed
    if (
        hasattr(sys, "XXstderrXX")
        and sys.stderr is not None
        and not (hasattr(sys.stderr, "closed") and sys.stderr.closed)
    ):
        return sys.stderr
    else:
        return io.StringIO()


def x_get_safe_stderr__mutmut_8() -> TextIO:
    """Get a safe stderr stream, falling back to StringIO if stderr is not available.

    This is used during initialization when sys.stderr might not be available
    (e.g., in some embedded Python environments or during testing).

    Returns:
        A writable text stream, either sys.stderr or io.StringIO()

    """
    # Check if stderr exists, is not None, and is not closed
    if (
        hasattr(sys, "STDERR")
        and sys.stderr is not None
        and not (hasattr(sys.stderr, "closed") and sys.stderr.closed)
    ):
        return sys.stderr
    else:
        return io.StringIO()


def x_get_safe_stderr__mutmut_9() -> TextIO:
    """Get a safe stderr stream, falling back to StringIO if stderr is not available.

    This is used during initialization when sys.stderr might not be available
    (e.g., in some embedded Python environments or during testing).

    Returns:
        A writable text stream, either sys.stderr or io.StringIO()

    """
    # Check if stderr exists, is not None, and is not closed
    if (
        hasattr(sys, "stderr")
        and sys.stderr is None
        and not (hasattr(sys.stderr, "closed") and sys.stderr.closed)
    ):
        return sys.stderr
    else:
        return io.StringIO()


def x_get_safe_stderr__mutmut_10() -> TextIO:
    """Get a safe stderr stream, falling back to StringIO if stderr is not available.

    This is used during initialization when sys.stderr might not be available
    (e.g., in some embedded Python environments or during testing).

    Returns:
        A writable text stream, either sys.stderr or io.StringIO()

    """
    # Check if stderr exists, is not None, and is not closed
    if (
        hasattr(sys, "stderr")
        and sys.stderr is not None
        and (hasattr(sys.stderr, "closed") and sys.stderr.closed)
    ):
        return sys.stderr
    else:
        return io.StringIO()


def x_get_safe_stderr__mutmut_11() -> TextIO:
    """Get a safe stderr stream, falling back to StringIO if stderr is not available.

    This is used during initialization when sys.stderr might not be available
    (e.g., in some embedded Python environments or during testing).

    Returns:
        A writable text stream, either sys.stderr or io.StringIO()

    """
    # Check if stderr exists, is not None, and is not closed
    if (
        hasattr(sys, "stderr")
        and sys.stderr is not None
        and not (hasattr(sys.stderr, "closed") or sys.stderr.closed)
    ):
        return sys.stderr
    else:
        return io.StringIO()


def x_get_safe_stderr__mutmut_12() -> TextIO:
    """Get a safe stderr stream, falling back to StringIO if stderr is not available.

    This is used during initialization when sys.stderr might not be available
    (e.g., in some embedded Python environments or during testing).

    Returns:
        A writable text stream, either sys.stderr or io.StringIO()

    """
    # Check if stderr exists, is not None, and is not closed
    if (
        hasattr(sys, "stderr")
        and sys.stderr is not None
        and not (hasattr(None, "closed") and sys.stderr.closed)
    ):
        return sys.stderr
    else:
        return io.StringIO()


def x_get_safe_stderr__mutmut_13() -> TextIO:
    """Get a safe stderr stream, falling back to StringIO if stderr is not available.

    This is used during initialization when sys.stderr might not be available
    (e.g., in some embedded Python environments or during testing).

    Returns:
        A writable text stream, either sys.stderr or io.StringIO()

    """
    # Check if stderr exists, is not None, and is not closed
    if (
        hasattr(sys, "stderr")
        and sys.stderr is not None
        and not (hasattr(sys.stderr, None) and sys.stderr.closed)
    ):
        return sys.stderr
    else:
        return io.StringIO()


def x_get_safe_stderr__mutmut_14() -> TextIO:
    """Get a safe stderr stream, falling back to StringIO if stderr is not available.

    This is used during initialization when sys.stderr might not be available
    (e.g., in some embedded Python environments or during testing).

    Returns:
        A writable text stream, either sys.stderr or io.StringIO()

    """
    # Check if stderr exists, is not None, and is not closed
    if (
        hasattr(sys, "stderr")
        and sys.stderr is not None
        and not (hasattr("closed") and sys.stderr.closed)
    ):
        return sys.stderr
    else:
        return io.StringIO()


def x_get_safe_stderr__mutmut_15() -> TextIO:
    """Get a safe stderr stream, falling back to StringIO if stderr is not available.

    This is used during initialization when sys.stderr might not be available
    (e.g., in some embedded Python environments or during testing).

    Returns:
        A writable text stream, either sys.stderr or io.StringIO()

    """
    # Check if stderr exists, is not None, and is not closed
    if (
        hasattr(sys, "stderr")
        and sys.stderr is not None
        and not (hasattr(sys.stderr, ) and sys.stderr.closed)
    ):
        return sys.stderr
    else:
        return io.StringIO()


def x_get_safe_stderr__mutmut_16() -> TextIO:
    """Get a safe stderr stream, falling back to StringIO if stderr is not available.

    This is used during initialization when sys.stderr might not be available
    (e.g., in some embedded Python environments or during testing).

    Returns:
        A writable text stream, either sys.stderr or io.StringIO()

    """
    # Check if stderr exists, is not None, and is not closed
    if (
        hasattr(sys, "stderr")
        and sys.stderr is not None
        and not (hasattr(sys.stderr, "XXclosedXX") and sys.stderr.closed)
    ):
        return sys.stderr
    else:
        return io.StringIO()


def x_get_safe_stderr__mutmut_17() -> TextIO:
    """Get a safe stderr stream, falling back to StringIO if stderr is not available.

    This is used during initialization when sys.stderr might not be available
    (e.g., in some embedded Python environments or during testing).

    Returns:
        A writable text stream, either sys.stderr or io.StringIO()

    """
    # Check if stderr exists, is not None, and is not closed
    if (
        hasattr(sys, "stderr")
        and sys.stderr is not None
        and not (hasattr(sys.stderr, "CLOSED") and sys.stderr.closed)
    ):
        return sys.stderr
    else:
        return io.StringIO()

x_get_safe_stderr__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_safe_stderr__mutmut_1': x_get_safe_stderr__mutmut_1, 
    'x_get_safe_stderr__mutmut_2': x_get_safe_stderr__mutmut_2, 
    'x_get_safe_stderr__mutmut_3': x_get_safe_stderr__mutmut_3, 
    'x_get_safe_stderr__mutmut_4': x_get_safe_stderr__mutmut_4, 
    'x_get_safe_stderr__mutmut_5': x_get_safe_stderr__mutmut_5, 
    'x_get_safe_stderr__mutmut_6': x_get_safe_stderr__mutmut_6, 
    'x_get_safe_stderr__mutmut_7': x_get_safe_stderr__mutmut_7, 
    'x_get_safe_stderr__mutmut_8': x_get_safe_stderr__mutmut_8, 
    'x_get_safe_stderr__mutmut_9': x_get_safe_stderr__mutmut_9, 
    'x_get_safe_stderr__mutmut_10': x_get_safe_stderr__mutmut_10, 
    'x_get_safe_stderr__mutmut_11': x_get_safe_stderr__mutmut_11, 
    'x_get_safe_stderr__mutmut_12': x_get_safe_stderr__mutmut_12, 
    'x_get_safe_stderr__mutmut_13': x_get_safe_stderr__mutmut_13, 
    'x_get_safe_stderr__mutmut_14': x_get_safe_stderr__mutmut_14, 
    'x_get_safe_stderr__mutmut_15': x_get_safe_stderr__mutmut_15, 
    'x_get_safe_stderr__mutmut_16': x_get_safe_stderr__mutmut_16, 
    'x_get_safe_stderr__mutmut_17': x_get_safe_stderr__mutmut_17
}

def get_safe_stderr(*args, **kwargs):
    result = _mutmut_trampoline(x_get_safe_stderr__mutmut_orig, x_get_safe_stderr__mutmut_mutants, args, kwargs)
    return result 

get_safe_stderr.__signature__ = _mutmut_signature(x_get_safe_stderr__mutmut_orig)
x_get_safe_stderr__mutmut_orig.__name__ = 'x_get_safe_stderr'


def x_get_foundation_log_stream__mutmut_orig(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                invalid_value=output_setting,
                valid_options=["stderr", "stdout", "main"],
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_1(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting != "stdout":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                invalid_value=output_setting,
                valid_options=["stderr", "stdout", "main"],
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_2(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "XXstdoutXX":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                invalid_value=output_setting,
                valid_options=["stderr", "stdout", "main"],
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_3(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "STDOUT":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                invalid_value=output_setting,
                valid_options=["stderr", "stdout", "main"],
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_4(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting != "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                invalid_value=output_setting,
                valid_options=["stderr", "stdout", "main"],
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_5(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting == "XXmainXX":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                invalid_value=output_setting,
                valid_options=["stderr", "stdout", "main"],
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_6(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting == "MAIN":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                invalid_value=output_setting,
                valid_options=["stderr", "stdout", "main"],
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_7(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting != "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                invalid_value=output_setting,
                valid_options=["stderr", "stdout", "main"],
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_8(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "XXstderrXX":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                invalid_value=output_setting,
                valid_options=["stderr", "stdout", "main"],
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_9(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "STDERR":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                invalid_value=output_setting,
                valid_options=["stderr", "stdout", "main"],
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_10(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                None,
                invalid_value=output_setting,
                valid_options=["stderr", "stdout", "main"],
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_11(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                invalid_value=None,
                valid_options=["stderr", "stdout", "main"],
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_12(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                invalid_value=output_setting,
                valid_options=None,
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_13(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                invalid_value=output_setting,
                valid_options=["stderr", "stdout", "main"],
                default_used=None,
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_14(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                invalid_value=output_setting,
                valid_options=["stderr", "stdout", "main"],
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_15(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                valid_options=["stderr", "stdout", "main"],
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_16(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                invalid_value=output_setting,
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_17(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                invalid_value=output_setting,
                valid_options=["stderr", "stdout", "main"],
                )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_18(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "XX[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderrXX",
                invalid_value=output_setting,
                valid_options=["stderr", "stdout", "main"],
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_19(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[foundation config warning] invalid foundation_log_output value, using stderr",
                invalid_value=output_setting,
                valid_options=["stderr", "stdout", "main"],
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_20(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[FOUNDATION CONFIG WARNING] INVALID FOUNDATION_LOG_OUTPUT VALUE, USING STDERR",
                invalid_value=output_setting,
                valid_options=["stderr", "stdout", "main"],
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_21(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                invalid_value=output_setting,
                valid_options=["XXstderrXX", "stdout", "main"],
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_22(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                invalid_value=output_setting,
                valid_options=["STDERR", "stdout", "main"],
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_23(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                invalid_value=output_setting,
                valid_options=["stderr", "XXstdoutXX", "main"],
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_24(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                invalid_value=output_setting,
                valid_options=["stderr", "STDOUT", "main"],
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_25(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                invalid_value=output_setting,
                valid_options=["stderr", "stdout", "XXmainXX"],
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_26(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                invalid_value=output_setting,
                valid_options=["stderr", "stdout", "MAIN"],
                default_used="stderr",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_27(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                invalid_value=output_setting,
                valid_options=["stderr", "stdout", "main"],
                default_used="XXstderrXX",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()


def x_get_foundation_log_stream__mutmut_28(output_setting: str) -> TextIO:
    """Get the appropriate stream for Foundation internal logging.

    Args:
        output_setting: One of "stderr", "stdout", or "main"

    Returns:
        A writable text stream based on the output setting

    Notes:
        - "stderr": Returns sys.stderr (default, RPC-safe)
        - "stdout": Returns sys.stdout
        - "main": Returns the main logger stream from _PROVIDE_LOG_STREAM
        - Invalid values default to sys.stderr with warning

    """
    if output_setting == "stdout":
        return sys.stdout
    if output_setting == "main":
        # Import here to avoid circular dependency
        try:
            from provide.foundation.streams import get_log_stream

            return get_log_stream()
        except ImportError:
            # Fallback if setup module not available during initialization
            return get_safe_stderr()
    elif output_setting == "stderr":
        return get_safe_stderr()
    else:
        # Invalid value - warn and default to stderr
        # Import config logger here to avoid circular dependency
        try:
            from provide.foundation.logger.config.base import get_config_logger

            get_config_logger().warning(
                "[Foundation Config Warning] Invalid FOUNDATION_LOG_OUTPUT value, using stderr",
                invalid_value=output_setting,
                valid_options=["stderr", "stdout", "main"],
                default_used="STDERR",
            )
        except ImportError:
            # During early initialization, just use stderr silently
            pass
        return get_safe_stderr()

x_get_foundation_log_stream__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_foundation_log_stream__mutmut_1': x_get_foundation_log_stream__mutmut_1, 
    'x_get_foundation_log_stream__mutmut_2': x_get_foundation_log_stream__mutmut_2, 
    'x_get_foundation_log_stream__mutmut_3': x_get_foundation_log_stream__mutmut_3, 
    'x_get_foundation_log_stream__mutmut_4': x_get_foundation_log_stream__mutmut_4, 
    'x_get_foundation_log_stream__mutmut_5': x_get_foundation_log_stream__mutmut_5, 
    'x_get_foundation_log_stream__mutmut_6': x_get_foundation_log_stream__mutmut_6, 
    'x_get_foundation_log_stream__mutmut_7': x_get_foundation_log_stream__mutmut_7, 
    'x_get_foundation_log_stream__mutmut_8': x_get_foundation_log_stream__mutmut_8, 
    'x_get_foundation_log_stream__mutmut_9': x_get_foundation_log_stream__mutmut_9, 
    'x_get_foundation_log_stream__mutmut_10': x_get_foundation_log_stream__mutmut_10, 
    'x_get_foundation_log_stream__mutmut_11': x_get_foundation_log_stream__mutmut_11, 
    'x_get_foundation_log_stream__mutmut_12': x_get_foundation_log_stream__mutmut_12, 
    'x_get_foundation_log_stream__mutmut_13': x_get_foundation_log_stream__mutmut_13, 
    'x_get_foundation_log_stream__mutmut_14': x_get_foundation_log_stream__mutmut_14, 
    'x_get_foundation_log_stream__mutmut_15': x_get_foundation_log_stream__mutmut_15, 
    'x_get_foundation_log_stream__mutmut_16': x_get_foundation_log_stream__mutmut_16, 
    'x_get_foundation_log_stream__mutmut_17': x_get_foundation_log_stream__mutmut_17, 
    'x_get_foundation_log_stream__mutmut_18': x_get_foundation_log_stream__mutmut_18, 
    'x_get_foundation_log_stream__mutmut_19': x_get_foundation_log_stream__mutmut_19, 
    'x_get_foundation_log_stream__mutmut_20': x_get_foundation_log_stream__mutmut_20, 
    'x_get_foundation_log_stream__mutmut_21': x_get_foundation_log_stream__mutmut_21, 
    'x_get_foundation_log_stream__mutmut_22': x_get_foundation_log_stream__mutmut_22, 
    'x_get_foundation_log_stream__mutmut_23': x_get_foundation_log_stream__mutmut_23, 
    'x_get_foundation_log_stream__mutmut_24': x_get_foundation_log_stream__mutmut_24, 
    'x_get_foundation_log_stream__mutmut_25': x_get_foundation_log_stream__mutmut_25, 
    'x_get_foundation_log_stream__mutmut_26': x_get_foundation_log_stream__mutmut_26, 
    'x_get_foundation_log_stream__mutmut_27': x_get_foundation_log_stream__mutmut_27, 
    'x_get_foundation_log_stream__mutmut_28': x_get_foundation_log_stream__mutmut_28
}

def get_foundation_log_stream(*args, **kwargs):
    result = _mutmut_trampoline(x_get_foundation_log_stream__mutmut_orig, x_get_foundation_log_stream__mutmut_mutants, args, kwargs)
    return result 

get_foundation_log_stream.__signature__ = _mutmut_signature(x_get_foundation_log_stream__mutmut_orig)
x_get_foundation_log_stream__mutmut_orig.__name__ = 'x_get_foundation_log_stream'


# <3 🧱🤝🧰🪄
