# provide/foundation/streams/file.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

#
# file.py
#
import contextlib
import io
from pathlib import Path
import sys

from provide.foundation.streams.core import (
    _get_stream_lock,
    _reconfigure_structlog_stream,
)
from provide.foundation.utils.streams import get_safe_stderr

"""File stream management for Foundation.
Handles file-based logging streams and file operations.
"""
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


def x__safe_error_output__mutmut_orig(message: str) -> None:
    """Output error message to stderr using basic print to avoid circular dependencies.

    This function intentionally uses print() instead of Foundation's perr() to prevent
    circular import issues during stream initialization and teardown phases.
    """
    print(message, file=sys.stderr)


def x__safe_error_output__mutmut_1(message: str) -> None:
    """Output error message to stderr using basic print to avoid circular dependencies.

    This function intentionally uses print() instead of Foundation's perr() to prevent
    circular import issues during stream initialization and teardown phases.
    """
    print(None, file=sys.stderr)


def x__safe_error_output__mutmut_2(message: str) -> None:
    """Output error message to stderr using basic print to avoid circular dependencies.

    This function intentionally uses print() instead of Foundation's perr() to prevent
    circular import issues during stream initialization and teardown phases.
    """
    print(message, file=None)


def x__safe_error_output__mutmut_3(message: str) -> None:
    """Output error message to stderr using basic print to avoid circular dependencies.

    This function intentionally uses print() instead of Foundation's perr() to prevent
    circular import issues during stream initialization and teardown phases.
    """
    print(file=sys.stderr)


def x__safe_error_output__mutmut_4(message: str) -> None:
    """Output error message to stderr using basic print to avoid circular dependencies.

    This function intentionally uses print() instead of Foundation's perr() to prevent
    circular import issues during stream initialization and teardown phases.
    """
    print(message, )

x__safe_error_output__mutmut_mutants : ClassVar[MutantDict] = {
'x__safe_error_output__mutmut_1': x__safe_error_output__mutmut_1, 
    'x__safe_error_output__mutmut_2': x__safe_error_output__mutmut_2, 
    'x__safe_error_output__mutmut_3': x__safe_error_output__mutmut_3, 
    'x__safe_error_output__mutmut_4': x__safe_error_output__mutmut_4
}

def _safe_error_output(*args, **kwargs):
    result = _mutmut_trampoline(x__safe_error_output__mutmut_orig, x__safe_error_output__mutmut_mutants, args, kwargs)
    return result 

_safe_error_output.__signature__ = _mutmut_signature(x__safe_error_output__mutmut_orig)
x__safe_error_output__mutmut_orig.__name__ = 'x__safe_error_output'


def x_configure_file_logging__mutmut_orig(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_1(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE or core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_2(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_3(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(None):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_4(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = ""

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_5(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = None

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_6(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr or not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_7(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_8(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_9(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=None, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_10(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=None)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_11(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_12(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, )
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_13(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(None).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_14(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=False, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_15(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=False)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_16(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = None  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_17(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open(None, encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_18(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding=None, buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_19(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="utf-8", buffering=None)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_20(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open(encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_21(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_22(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="utf-8", )  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_23(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(None).open("a", encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_24(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("XXaXX", encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_25(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("A", encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_26(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="XXutf-8XX", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_27(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="UTF-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_28(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="utf-8", buffering=2)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_29(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = None
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_30(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(None)
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_31(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = None
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_32(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif is_test_stream:
            core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_configure_file_logging__mutmut_33(log_file_path: str | None) -> None:
    """Configure file logging if a path is provided.

    Args:
        log_file_path: Path to log file, or None to disable file logging

    """
    # Import core module to modify the actual global variables
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        # Don't modify streams if we're in Click testing context
        if is_in_click_testing():
            return
        # Close existing file handle if it exists
        if (
            core_module._LOG_FILE_HANDLE
            and core_module._LOG_FILE_HANDLE is not core_module._PROVIDE_LOG_STREAM
        ):
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Check if we're in testing mode
        is_test_stream = core_module._PROVIDE_LOG_STREAM is not sys.stderr and not isinstance(
            core_module._PROVIDE_LOG_STREAM,
            io.TextIOWrapper,
        )

        if log_file_path:
            try:
                Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
                core_module._LOG_FILE_HANDLE = Path(log_file_path).open("a", encoding="utf-8", buffering=1)  # noqa: SIM115
                core_module._PROVIDE_LOG_STREAM = core_module._LOG_FILE_HANDLE
                # Reconfigure structlog to use the new file stream
                _reconfigure_structlog_stream()
            except Exception as e:
                # Log error to stderr and fall back
                _safe_error_output(f"Failed to open log file {log_file_path}: {e}")
                core_module._PROVIDE_LOG_STREAM = get_safe_stderr()
                # Reconfigure structlog to use stderr fallback
                _reconfigure_structlog_stream()
        elif not is_test_stream:
            core_module._PROVIDE_LOG_STREAM = None
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()

x_configure_file_logging__mutmut_mutants : ClassVar[MutantDict] = {
'x_configure_file_logging__mutmut_1': x_configure_file_logging__mutmut_1, 
    'x_configure_file_logging__mutmut_2': x_configure_file_logging__mutmut_2, 
    'x_configure_file_logging__mutmut_3': x_configure_file_logging__mutmut_3, 
    'x_configure_file_logging__mutmut_4': x_configure_file_logging__mutmut_4, 
    'x_configure_file_logging__mutmut_5': x_configure_file_logging__mutmut_5, 
    'x_configure_file_logging__mutmut_6': x_configure_file_logging__mutmut_6, 
    'x_configure_file_logging__mutmut_7': x_configure_file_logging__mutmut_7, 
    'x_configure_file_logging__mutmut_8': x_configure_file_logging__mutmut_8, 
    'x_configure_file_logging__mutmut_9': x_configure_file_logging__mutmut_9, 
    'x_configure_file_logging__mutmut_10': x_configure_file_logging__mutmut_10, 
    'x_configure_file_logging__mutmut_11': x_configure_file_logging__mutmut_11, 
    'x_configure_file_logging__mutmut_12': x_configure_file_logging__mutmut_12, 
    'x_configure_file_logging__mutmut_13': x_configure_file_logging__mutmut_13, 
    'x_configure_file_logging__mutmut_14': x_configure_file_logging__mutmut_14, 
    'x_configure_file_logging__mutmut_15': x_configure_file_logging__mutmut_15, 
    'x_configure_file_logging__mutmut_16': x_configure_file_logging__mutmut_16, 
    'x_configure_file_logging__mutmut_17': x_configure_file_logging__mutmut_17, 
    'x_configure_file_logging__mutmut_18': x_configure_file_logging__mutmut_18, 
    'x_configure_file_logging__mutmut_19': x_configure_file_logging__mutmut_19, 
    'x_configure_file_logging__mutmut_20': x_configure_file_logging__mutmut_20, 
    'x_configure_file_logging__mutmut_21': x_configure_file_logging__mutmut_21, 
    'x_configure_file_logging__mutmut_22': x_configure_file_logging__mutmut_22, 
    'x_configure_file_logging__mutmut_23': x_configure_file_logging__mutmut_23, 
    'x_configure_file_logging__mutmut_24': x_configure_file_logging__mutmut_24, 
    'x_configure_file_logging__mutmut_25': x_configure_file_logging__mutmut_25, 
    'x_configure_file_logging__mutmut_26': x_configure_file_logging__mutmut_26, 
    'x_configure_file_logging__mutmut_27': x_configure_file_logging__mutmut_27, 
    'x_configure_file_logging__mutmut_28': x_configure_file_logging__mutmut_28, 
    'x_configure_file_logging__mutmut_29': x_configure_file_logging__mutmut_29, 
    'x_configure_file_logging__mutmut_30': x_configure_file_logging__mutmut_30, 
    'x_configure_file_logging__mutmut_31': x_configure_file_logging__mutmut_31, 
    'x_configure_file_logging__mutmut_32': x_configure_file_logging__mutmut_32, 
    'x_configure_file_logging__mutmut_33': x_configure_file_logging__mutmut_33
}

def configure_file_logging(*args, **kwargs):
    result = _mutmut_trampoline(x_configure_file_logging__mutmut_orig, x_configure_file_logging__mutmut_mutants, args, kwargs)
    return result 

configure_file_logging.__signature__ = _mutmut_signature(x_configure_file_logging__mutmut_orig)
x_configure_file_logging__mutmut_orig.__name__ = 'x_configure_file_logging'


def x_flush_log_streams__mutmut_orig() -> None:
    """Flush all log streams."""
    import provide.foundation.streams.core as core_module

    with _get_stream_lock():
        if core_module._LOG_FILE_HANDLE:
            try:
                core_module._LOG_FILE_HANDLE.flush()
            except Exception as e:
                _safe_error_output(f"Failed to flush log file handle: {e}")


def x_flush_log_streams__mutmut_1() -> None:
    """Flush all log streams."""
    import provide.foundation.streams.core as core_module

    with _get_stream_lock():
        if core_module._LOG_FILE_HANDLE:
            try:
                core_module._LOG_FILE_HANDLE.flush()
            except Exception as e:
                _safe_error_output(None)

x_flush_log_streams__mutmut_mutants : ClassVar[MutantDict] = {
'x_flush_log_streams__mutmut_1': x_flush_log_streams__mutmut_1
}

def flush_log_streams(*args, **kwargs):
    result = _mutmut_trampoline(x_flush_log_streams__mutmut_orig, x_flush_log_streams__mutmut_mutants, args, kwargs)
    return result 

flush_log_streams.__signature__ = _mutmut_signature(x_flush_log_streams__mutmut_orig)
x_flush_log_streams__mutmut_orig.__name__ = 'x_flush_log_streams'


def x_close_log_streams__mutmut_orig() -> None:
    """Close file log streams and reset to stderr."""
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        if core_module._LOG_FILE_HANDLE:
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Don't reset stream to stderr if we're in Click testing context
        if not is_in_click_testing():
            core_module._PROVIDE_LOG_STREAM = sys.stderr
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_close_log_streams__mutmut_1() -> None:
    """Close file log streams and reset to stderr."""
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        if core_module._LOG_FILE_HANDLE:
            with contextlib.suppress(None):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Don't reset stream to stderr if we're in Click testing context
        if not is_in_click_testing():
            core_module._PROVIDE_LOG_STREAM = sys.stderr
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_close_log_streams__mutmut_2() -> None:
    """Close file log streams and reset to stderr."""
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        if core_module._LOG_FILE_HANDLE:
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = ""

        # Don't reset stream to stderr if we're in Click testing context
        if not is_in_click_testing():
            core_module._PROVIDE_LOG_STREAM = sys.stderr
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_close_log_streams__mutmut_3() -> None:
    """Close file log streams and reset to stderr."""
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        if core_module._LOG_FILE_HANDLE:
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Don't reset stream to stderr if we're in Click testing context
        if is_in_click_testing():
            core_module._PROVIDE_LOG_STREAM = sys.stderr
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()


def x_close_log_streams__mutmut_4() -> None:
    """Close file log streams and reset to stderr."""
    import provide.foundation.streams.core as core_module

    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    with _get_stream_lock():
        if core_module._LOG_FILE_HANDLE:
            with contextlib.suppress(Exception):
                core_module._LOG_FILE_HANDLE.close()
            core_module._LOG_FILE_HANDLE = None

        # Don't reset stream to stderr if we're in Click testing context
        if not is_in_click_testing():
            core_module._PROVIDE_LOG_STREAM = None
            # Reconfigure structlog to use stderr
            _reconfigure_structlog_stream()

x_close_log_streams__mutmut_mutants : ClassVar[MutantDict] = {
'x_close_log_streams__mutmut_1': x_close_log_streams__mutmut_1, 
    'x_close_log_streams__mutmut_2': x_close_log_streams__mutmut_2, 
    'x_close_log_streams__mutmut_3': x_close_log_streams__mutmut_3, 
    'x_close_log_streams__mutmut_4': x_close_log_streams__mutmut_4
}

def close_log_streams(*args, **kwargs):
    result = _mutmut_trampoline(x_close_log_streams__mutmut_orig, x_close_log_streams__mutmut_mutants, args, kwargs)
    return result 

close_log_streams.__signature__ = _mutmut_signature(x_close_log_streams__mutmut_orig)
x_close_log_streams__mutmut_orig.__name__ = 'x_close_log_streams'


def x_reset_streams__mutmut_orig() -> None:
    """Reset all stream state (for testing)."""
    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    # Don't reset streams if we're in Click testing context
    if not is_in_click_testing():
        close_log_streams()


def x_reset_streams__mutmut_1() -> None:
    """Reset all stream state (for testing)."""
    # Import here to avoid circular dependency
    from provide.foundation.testmode.detection import is_in_click_testing

    # Don't reset streams if we're in Click testing context
    if is_in_click_testing():
        close_log_streams()

x_reset_streams__mutmut_mutants : ClassVar[MutantDict] = {
'x_reset_streams__mutmut_1': x_reset_streams__mutmut_1
}

def reset_streams(*args, **kwargs):
    result = _mutmut_trampoline(x_reset_streams__mutmut_orig, x_reset_streams__mutmut_mutants, args, kwargs)
    return result 

reset_streams.__signature__ = _mutmut_signature(x_reset_streams__mutmut_orig)
x_reset_streams__mutmut_orig.__name__ = 'x_reset_streams'


# <3 🧱🤝🌊🪄
