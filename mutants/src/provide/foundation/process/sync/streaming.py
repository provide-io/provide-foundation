# provide/foundation/process/sync/streaming.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from collections.abc import Iterator, Mapping
from pathlib import Path
import subprocess
from typing import Any

from provide.foundation.errors.process import ProcessError, ProcessTimeoutError
from provide.foundation.logger import get_logger
from provide.foundation.process.shared import normalize_cwd, prepare_environment

"""Sync subprocess streaming execution."""

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


def x__make_stdout_nonblocking__mutmut_orig(stdout: Any) -> None:
    """Make stdout non-blocking for timeout handling."""
    import fcntl
    import os

    fd = stdout.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)


def x__make_stdout_nonblocking__mutmut_1(stdout: Any) -> None:
    """Make stdout non-blocking for timeout handling."""
    import fcntl
    import os

    fd = None
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)


def x__make_stdout_nonblocking__mutmut_2(stdout: Any) -> None:
    """Make stdout non-blocking for timeout handling."""
    import fcntl
    import os

    fd = stdout.fileno()
    fl = None
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)


def x__make_stdout_nonblocking__mutmut_3(stdout: Any) -> None:
    """Make stdout non-blocking for timeout handling."""
    import fcntl
    import os

    fd = stdout.fileno()
    fl = fcntl.fcntl(None, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)


def x__make_stdout_nonblocking__mutmut_4(stdout: Any) -> None:
    """Make stdout non-blocking for timeout handling."""
    import fcntl
    import os

    fd = stdout.fileno()
    fl = fcntl.fcntl(fd, None)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)


def x__make_stdout_nonblocking__mutmut_5(stdout: Any) -> None:
    """Make stdout non-blocking for timeout handling."""
    import fcntl
    import os

    fd = stdout.fileno()
    fl = fcntl.fcntl(fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)


def x__make_stdout_nonblocking__mutmut_6(stdout: Any) -> None:
    """Make stdout non-blocking for timeout handling."""
    import fcntl
    import os

    fd = stdout.fileno()
    fl = fcntl.fcntl(fd, )
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)


def x__make_stdout_nonblocking__mutmut_7(stdout: Any) -> None:
    """Make stdout non-blocking for timeout handling."""
    import fcntl
    import os

    fd = stdout.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(None, fcntl.F_SETFL, fl | os.O_NONBLOCK)


def x__make_stdout_nonblocking__mutmut_8(stdout: Any) -> None:
    """Make stdout non-blocking for timeout handling."""
    import fcntl
    import os

    fd = stdout.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, None, fl | os.O_NONBLOCK)


def x__make_stdout_nonblocking__mutmut_9(stdout: Any) -> None:
    """Make stdout non-blocking for timeout handling."""
    import fcntl
    import os

    fd = stdout.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, None)


def x__make_stdout_nonblocking__mutmut_10(stdout: Any) -> None:
    """Make stdout non-blocking for timeout handling."""
    import fcntl
    import os

    fd = stdout.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fcntl.F_SETFL, fl | os.O_NONBLOCK)


def x__make_stdout_nonblocking__mutmut_11(stdout: Any) -> None:
    """Make stdout non-blocking for timeout handling."""
    import fcntl
    import os

    fd = stdout.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fl | os.O_NONBLOCK)


def x__make_stdout_nonblocking__mutmut_12(stdout: Any) -> None:
    """Make stdout non-blocking for timeout handling."""
    import fcntl
    import os

    fd = stdout.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, )


def x__make_stdout_nonblocking__mutmut_13(stdout: Any) -> None:
    """Make stdout non-blocking for timeout handling."""
    import fcntl
    import os

    fd = stdout.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl & os.O_NONBLOCK)

x__make_stdout_nonblocking__mutmut_mutants : ClassVar[MutantDict] = {
'x__make_stdout_nonblocking__mutmut_1': x__make_stdout_nonblocking__mutmut_1, 
    'x__make_stdout_nonblocking__mutmut_2': x__make_stdout_nonblocking__mutmut_2, 
    'x__make_stdout_nonblocking__mutmut_3': x__make_stdout_nonblocking__mutmut_3, 
    'x__make_stdout_nonblocking__mutmut_4': x__make_stdout_nonblocking__mutmut_4, 
    'x__make_stdout_nonblocking__mutmut_5': x__make_stdout_nonblocking__mutmut_5, 
    'x__make_stdout_nonblocking__mutmut_6': x__make_stdout_nonblocking__mutmut_6, 
    'x__make_stdout_nonblocking__mutmut_7': x__make_stdout_nonblocking__mutmut_7, 
    'x__make_stdout_nonblocking__mutmut_8': x__make_stdout_nonblocking__mutmut_8, 
    'x__make_stdout_nonblocking__mutmut_9': x__make_stdout_nonblocking__mutmut_9, 
    'x__make_stdout_nonblocking__mutmut_10': x__make_stdout_nonblocking__mutmut_10, 
    'x__make_stdout_nonblocking__mutmut_11': x__make_stdout_nonblocking__mutmut_11, 
    'x__make_stdout_nonblocking__mutmut_12': x__make_stdout_nonblocking__mutmut_12, 
    'x__make_stdout_nonblocking__mutmut_13': x__make_stdout_nonblocking__mutmut_13
}

def _make_stdout_nonblocking(*args, **kwargs):
    result = _mutmut_trampoline(x__make_stdout_nonblocking__mutmut_orig, x__make_stdout_nonblocking__mutmut_mutants, args, kwargs)
    return result 

_make_stdout_nonblocking.__signature__ = _mutmut_signature(x__make_stdout_nonblocking__mutmut_orig)
x__make_stdout_nonblocking__mutmut_orig.__name__ = 'x__make_stdout_nonblocking'


def x__check_timeout_expired__mutmut_orig(start_time: float, timeout: float, cmd_str: str, process: Any) -> None:
    """Check if timeout has expired and handle it."""
    import time

    elapsed = time.time() - start_time
    if elapsed >= timeout:
        process.kill()
        process.wait()
        log.error("⏱️ Stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        )


def x__check_timeout_expired__mutmut_1(start_time: float, timeout: float, cmd_str: str, process: Any) -> None:
    """Check if timeout has expired and handle it."""
    import time

    elapsed = None
    if elapsed >= timeout:
        process.kill()
        process.wait()
        log.error("⏱️ Stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        )


def x__check_timeout_expired__mutmut_2(start_time: float, timeout: float, cmd_str: str, process: Any) -> None:
    """Check if timeout has expired and handle it."""
    import time

    elapsed = time.time() + start_time
    if elapsed >= timeout:
        process.kill()
        process.wait()
        log.error("⏱️ Stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        )


def x__check_timeout_expired__mutmut_3(start_time: float, timeout: float, cmd_str: str, process: Any) -> None:
    """Check if timeout has expired and handle it."""
    import time

    elapsed = time.time() - start_time
    if elapsed > timeout:
        process.kill()
        process.wait()
        log.error("⏱️ Stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        )


def x__check_timeout_expired__mutmut_4(start_time: float, timeout: float, cmd_str: str, process: Any) -> None:
    """Check if timeout has expired and handle it."""
    import time

    elapsed = time.time() - start_time
    if elapsed >= timeout:
        process.kill()
        process.wait()
        log.error(None, command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        )


def x__check_timeout_expired__mutmut_5(start_time: float, timeout: float, cmd_str: str, process: Any) -> None:
    """Check if timeout has expired and handle it."""
    import time

    elapsed = time.time() - start_time
    if elapsed >= timeout:
        process.kill()
        process.wait()
        log.error("⏱️ Stream timed out", command=None, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        )


def x__check_timeout_expired__mutmut_6(start_time: float, timeout: float, cmd_str: str, process: Any) -> None:
    """Check if timeout has expired and handle it."""
    import time

    elapsed = time.time() - start_time
    if elapsed >= timeout:
        process.kill()
        process.wait()
        log.error("⏱️ Stream timed out", command=cmd_str, timeout=None)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        )


def x__check_timeout_expired__mutmut_7(start_time: float, timeout: float, cmd_str: str, process: Any) -> None:
    """Check if timeout has expired and handle it."""
    import time

    elapsed = time.time() - start_time
    if elapsed >= timeout:
        process.kill()
        process.wait()
        log.error(command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        )


def x__check_timeout_expired__mutmut_8(start_time: float, timeout: float, cmd_str: str, process: Any) -> None:
    """Check if timeout has expired and handle it."""
    import time

    elapsed = time.time() - start_time
    if elapsed >= timeout:
        process.kill()
        process.wait()
        log.error("⏱️ Stream timed out", timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        )


def x__check_timeout_expired__mutmut_9(start_time: float, timeout: float, cmd_str: str, process: Any) -> None:
    """Check if timeout has expired and handle it."""
    import time

    elapsed = time.time() - start_time
    if elapsed >= timeout:
        process.kill()
        process.wait()
        log.error("⏱️ Stream timed out", command=cmd_str, )
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        )


def x__check_timeout_expired__mutmut_10(start_time: float, timeout: float, cmd_str: str, process: Any) -> None:
    """Check if timeout has expired and handle it."""
    import time

    elapsed = time.time() - start_time
    if elapsed >= timeout:
        process.kill()
        process.wait()
        log.error("XX⏱️ Stream timed outXX", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        )


def x__check_timeout_expired__mutmut_11(start_time: float, timeout: float, cmd_str: str, process: Any) -> None:
    """Check if timeout has expired and handle it."""
    import time

    elapsed = time.time() - start_time
    if elapsed >= timeout:
        process.kill()
        process.wait()
        log.error("⏱️ stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        )


def x__check_timeout_expired__mutmut_12(start_time: float, timeout: float, cmd_str: str, process: Any) -> None:
    """Check if timeout has expired and handle it."""
    import time

    elapsed = time.time() - start_time
    if elapsed >= timeout:
        process.kill()
        process.wait()
        log.error("⏱️ STREAM TIMED OUT", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        )


def x__check_timeout_expired__mutmut_13(start_time: float, timeout: float, cmd_str: str, process: Any) -> None:
    """Check if timeout has expired and handle it."""
    import time

    elapsed = time.time() - start_time
    if elapsed >= timeout:
        process.kill()
        process.wait()
        log.error("⏱️ Stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            None,
            code="PROCESS_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        )


def x__check_timeout_expired__mutmut_14(start_time: float, timeout: float, cmd_str: str, process: Any) -> None:
    """Check if timeout has expired and handle it."""
    import time

    elapsed = time.time() - start_time
    if elapsed >= timeout:
        process.kill()
        process.wait()
        log.error("⏱️ Stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code=None,
            command=cmd_str,
            timeout_seconds=timeout,
        )


def x__check_timeout_expired__mutmut_15(start_time: float, timeout: float, cmd_str: str, process: Any) -> None:
    """Check if timeout has expired and handle it."""
    import time

    elapsed = time.time() - start_time
    if elapsed >= timeout:
        process.kill()
        process.wait()
        log.error("⏱️ Stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_STREAM_TIMEOUT",
            command=None,
            timeout_seconds=timeout,
        )


def x__check_timeout_expired__mutmut_16(start_time: float, timeout: float, cmd_str: str, process: Any) -> None:
    """Check if timeout has expired and handle it."""
    import time

    elapsed = time.time() - start_time
    if elapsed >= timeout:
        process.kill()
        process.wait()
        log.error("⏱️ Stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=None,
        )


def x__check_timeout_expired__mutmut_17(start_time: float, timeout: float, cmd_str: str, process: Any) -> None:
    """Check if timeout has expired and handle it."""
    import time

    elapsed = time.time() - start_time
    if elapsed >= timeout:
        process.kill()
        process.wait()
        log.error("⏱️ Stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            code="PROCESS_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        )


def x__check_timeout_expired__mutmut_18(start_time: float, timeout: float, cmd_str: str, process: Any) -> None:
    """Check if timeout has expired and handle it."""
    import time

    elapsed = time.time() - start_time
    if elapsed >= timeout:
        process.kill()
        process.wait()
        log.error("⏱️ Stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            command=cmd_str,
            timeout_seconds=timeout,
        )


def x__check_timeout_expired__mutmut_19(start_time: float, timeout: float, cmd_str: str, process: Any) -> None:
    """Check if timeout has expired and handle it."""
    import time

    elapsed = time.time() - start_time
    if elapsed >= timeout:
        process.kill()
        process.wait()
        log.error("⏱️ Stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_STREAM_TIMEOUT",
            timeout_seconds=timeout,
        )


def x__check_timeout_expired__mutmut_20(start_time: float, timeout: float, cmd_str: str, process: Any) -> None:
    """Check if timeout has expired and handle it."""
    import time

    elapsed = time.time() - start_time
    if elapsed >= timeout:
        process.kill()
        process.wait()
        log.error("⏱️ Stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_STREAM_TIMEOUT",
            command=cmd_str,
            )


def x__check_timeout_expired__mutmut_21(start_time: float, timeout: float, cmd_str: str, process: Any) -> None:
    """Check if timeout has expired and handle it."""
    import time

    elapsed = time.time() - start_time
    if elapsed >= timeout:
        process.kill()
        process.wait()
        log.error("⏱️ Stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="XXPROCESS_STREAM_TIMEOUTXX",
            command=cmd_str,
            timeout_seconds=timeout,
        )


def x__check_timeout_expired__mutmut_22(start_time: float, timeout: float, cmd_str: str, process: Any) -> None:
    """Check if timeout has expired and handle it."""
    import time

    elapsed = time.time() - start_time
    if elapsed >= timeout:
        process.kill()
        process.wait()
        log.error("⏱️ Stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="process_stream_timeout",
            command=cmd_str,
            timeout_seconds=timeout,
        )

x__check_timeout_expired__mutmut_mutants : ClassVar[MutantDict] = {
'x__check_timeout_expired__mutmut_1': x__check_timeout_expired__mutmut_1, 
    'x__check_timeout_expired__mutmut_2': x__check_timeout_expired__mutmut_2, 
    'x__check_timeout_expired__mutmut_3': x__check_timeout_expired__mutmut_3, 
    'x__check_timeout_expired__mutmut_4': x__check_timeout_expired__mutmut_4, 
    'x__check_timeout_expired__mutmut_5': x__check_timeout_expired__mutmut_5, 
    'x__check_timeout_expired__mutmut_6': x__check_timeout_expired__mutmut_6, 
    'x__check_timeout_expired__mutmut_7': x__check_timeout_expired__mutmut_7, 
    'x__check_timeout_expired__mutmut_8': x__check_timeout_expired__mutmut_8, 
    'x__check_timeout_expired__mutmut_9': x__check_timeout_expired__mutmut_9, 
    'x__check_timeout_expired__mutmut_10': x__check_timeout_expired__mutmut_10, 
    'x__check_timeout_expired__mutmut_11': x__check_timeout_expired__mutmut_11, 
    'x__check_timeout_expired__mutmut_12': x__check_timeout_expired__mutmut_12, 
    'x__check_timeout_expired__mutmut_13': x__check_timeout_expired__mutmut_13, 
    'x__check_timeout_expired__mutmut_14': x__check_timeout_expired__mutmut_14, 
    'x__check_timeout_expired__mutmut_15': x__check_timeout_expired__mutmut_15, 
    'x__check_timeout_expired__mutmut_16': x__check_timeout_expired__mutmut_16, 
    'x__check_timeout_expired__mutmut_17': x__check_timeout_expired__mutmut_17, 
    'x__check_timeout_expired__mutmut_18': x__check_timeout_expired__mutmut_18, 
    'x__check_timeout_expired__mutmut_19': x__check_timeout_expired__mutmut_19, 
    'x__check_timeout_expired__mutmut_20': x__check_timeout_expired__mutmut_20, 
    'x__check_timeout_expired__mutmut_21': x__check_timeout_expired__mutmut_21, 
    'x__check_timeout_expired__mutmut_22': x__check_timeout_expired__mutmut_22
}

def _check_timeout_expired(*args, **kwargs):
    result = _mutmut_trampoline(x__check_timeout_expired__mutmut_orig, x__check_timeout_expired__mutmut_mutants, args, kwargs)
    return result 

_check_timeout_expired.__signature__ = _mutmut_signature(x__check_timeout_expired__mutmut_orig)
x__check_timeout_expired__mutmut_orig.__name__ = 'x__check_timeout_expired'


def x__read_chunk_from_stdout__mutmut_orig(stdout: Any, buffer: str) -> tuple[str, bool]:
    """Read a chunk from stdout and update buffer. Returns (new_buffer, eof_reached)."""
    try:
        chunk = stdout.read(1024)
        if not chunk:
            return buffer, True  # EOF
        return buffer + chunk, False
    except OSError:
        # No data available yet
        return buffer, False


def x__read_chunk_from_stdout__mutmut_1(stdout: Any, buffer: str) -> tuple[str, bool]:
    """Read a chunk from stdout and update buffer. Returns (new_buffer, eof_reached)."""
    try:
        chunk = None
        if not chunk:
            return buffer, True  # EOF
        return buffer + chunk, False
    except OSError:
        # No data available yet
        return buffer, False


def x__read_chunk_from_stdout__mutmut_2(stdout: Any, buffer: str) -> tuple[str, bool]:
    """Read a chunk from stdout and update buffer. Returns (new_buffer, eof_reached)."""
    try:
        chunk = stdout.read(None)
        if not chunk:
            return buffer, True  # EOF
        return buffer + chunk, False
    except OSError:
        # No data available yet
        return buffer, False


def x__read_chunk_from_stdout__mutmut_3(stdout: Any, buffer: str) -> tuple[str, bool]:
    """Read a chunk from stdout and update buffer. Returns (new_buffer, eof_reached)."""
    try:
        chunk = stdout.read(1025)
        if not chunk:
            return buffer, True  # EOF
        return buffer + chunk, False
    except OSError:
        # No data available yet
        return buffer, False


def x__read_chunk_from_stdout__mutmut_4(stdout: Any, buffer: str) -> tuple[str, bool]:
    """Read a chunk from stdout and update buffer. Returns (new_buffer, eof_reached)."""
    try:
        chunk = stdout.read(1024)
        if chunk:
            return buffer, True  # EOF
        return buffer + chunk, False
    except OSError:
        # No data available yet
        return buffer, False


def x__read_chunk_from_stdout__mutmut_5(stdout: Any, buffer: str) -> tuple[str, bool]:
    """Read a chunk from stdout and update buffer. Returns (new_buffer, eof_reached)."""
    try:
        chunk = stdout.read(1024)
        if not chunk:
            return buffer, False  # EOF
        return buffer + chunk, False
    except OSError:
        # No data available yet
        return buffer, False


def x__read_chunk_from_stdout__mutmut_6(stdout: Any, buffer: str) -> tuple[str, bool]:
    """Read a chunk from stdout and update buffer. Returns (new_buffer, eof_reached)."""
    try:
        chunk = stdout.read(1024)
        if not chunk:
            return buffer, True  # EOF
        return buffer - chunk, False
    except OSError:
        # No data available yet
        return buffer, False


def x__read_chunk_from_stdout__mutmut_7(stdout: Any, buffer: str) -> tuple[str, bool]:
    """Read a chunk from stdout and update buffer. Returns (new_buffer, eof_reached)."""
    try:
        chunk = stdout.read(1024)
        if not chunk:
            return buffer, True  # EOF
        return buffer + chunk, True
    except OSError:
        # No data available yet
        return buffer, False


def x__read_chunk_from_stdout__mutmut_8(stdout: Any, buffer: str) -> tuple[str, bool]:
    """Read a chunk from stdout and update buffer. Returns (new_buffer, eof_reached)."""
    try:
        chunk = stdout.read(1024)
        if not chunk:
            return buffer, True  # EOF
        return buffer + chunk, False
    except OSError:
        # No data available yet
        return buffer, True

x__read_chunk_from_stdout__mutmut_mutants : ClassVar[MutantDict] = {
'x__read_chunk_from_stdout__mutmut_1': x__read_chunk_from_stdout__mutmut_1, 
    'x__read_chunk_from_stdout__mutmut_2': x__read_chunk_from_stdout__mutmut_2, 
    'x__read_chunk_from_stdout__mutmut_3': x__read_chunk_from_stdout__mutmut_3, 
    'x__read_chunk_from_stdout__mutmut_4': x__read_chunk_from_stdout__mutmut_4, 
    'x__read_chunk_from_stdout__mutmut_5': x__read_chunk_from_stdout__mutmut_5, 
    'x__read_chunk_from_stdout__mutmut_6': x__read_chunk_from_stdout__mutmut_6, 
    'x__read_chunk_from_stdout__mutmut_7': x__read_chunk_from_stdout__mutmut_7, 
    'x__read_chunk_from_stdout__mutmut_8': x__read_chunk_from_stdout__mutmut_8
}

def _read_chunk_from_stdout(*args, **kwargs):
    result = _mutmut_trampoline(x__read_chunk_from_stdout__mutmut_orig, x__read_chunk_from_stdout__mutmut_mutants, args, kwargs)
    return result 

_read_chunk_from_stdout.__signature__ = _mutmut_signature(x__read_chunk_from_stdout__mutmut_orig)
x__read_chunk_from_stdout__mutmut_orig.__name__ = 'x__read_chunk_from_stdout'


def x__yield_complete_lines__mutmut_orig(buffer: str) -> Iterator[tuple[str, str]]:
    """Yield complete lines from buffer. Returns (line, remaining_buffer) tuples."""
    while "\n" in buffer:
        line, buffer = buffer.split("\n", 1)
        yield line.rstrip(), buffer


def x__yield_complete_lines__mutmut_1(buffer: str) -> Iterator[tuple[str, str]]:
    """Yield complete lines from buffer. Returns (line, remaining_buffer) tuples."""
    while "XX\nXX" in buffer:
        line, buffer = buffer.split("\n", 1)
        yield line.rstrip(), buffer


def x__yield_complete_lines__mutmut_2(buffer: str) -> Iterator[tuple[str, str]]:
    """Yield complete lines from buffer. Returns (line, remaining_buffer) tuples."""
    while "\n" not in buffer:
        line, buffer = buffer.split("\n", 1)
        yield line.rstrip(), buffer


def x__yield_complete_lines__mutmut_3(buffer: str) -> Iterator[tuple[str, str]]:
    """Yield complete lines from buffer. Returns (line, remaining_buffer) tuples."""
    while "\n" in buffer:
        line, buffer = None
        yield line.rstrip(), buffer


def x__yield_complete_lines__mutmut_4(buffer: str) -> Iterator[tuple[str, str]]:
    """Yield complete lines from buffer. Returns (line, remaining_buffer) tuples."""
    while "\n" in buffer:
        line, buffer = buffer.split(None, 1)
        yield line.rstrip(), buffer


def x__yield_complete_lines__mutmut_5(buffer: str) -> Iterator[tuple[str, str]]:
    """Yield complete lines from buffer. Returns (line, remaining_buffer) tuples."""
    while "\n" in buffer:
        line, buffer = buffer.split("\n", None)
        yield line.rstrip(), buffer


def x__yield_complete_lines__mutmut_6(buffer: str) -> Iterator[tuple[str, str]]:
    """Yield complete lines from buffer. Returns (line, remaining_buffer) tuples."""
    while "\n" in buffer:
        line, buffer = buffer.split(1)
        yield line.rstrip(), buffer


def x__yield_complete_lines__mutmut_7(buffer: str) -> Iterator[tuple[str, str]]:
    """Yield complete lines from buffer. Returns (line, remaining_buffer) tuples."""
    while "\n" in buffer:
        line, buffer = buffer.split("\n", )
        yield line.rstrip(), buffer


def x__yield_complete_lines__mutmut_8(buffer: str) -> Iterator[tuple[str, str]]:
    """Yield complete lines from buffer. Returns (line, remaining_buffer) tuples."""
    while "\n" in buffer:
        line, buffer = buffer.rsplit("\n", 1)
        yield line.rstrip(), buffer


def x__yield_complete_lines__mutmut_9(buffer: str) -> Iterator[tuple[str, str]]:
    """Yield complete lines from buffer. Returns (line, remaining_buffer) tuples."""
    while "\n" in buffer:
        line, buffer = buffer.split("XX\nXX", 1)
        yield line.rstrip(), buffer


def x__yield_complete_lines__mutmut_10(buffer: str) -> Iterator[tuple[str, str]]:
    """Yield complete lines from buffer. Returns (line, remaining_buffer) tuples."""
    while "\n" in buffer:
        line, buffer = buffer.split("\n", 2)
        yield line.rstrip(), buffer


def x__yield_complete_lines__mutmut_11(buffer: str) -> Iterator[tuple[str, str]]:
    """Yield complete lines from buffer. Returns (line, remaining_buffer) tuples."""
    while "\n" in buffer:
        line, buffer = buffer.split("\n", 1)
        yield line.lstrip(), buffer

x__yield_complete_lines__mutmut_mutants : ClassVar[MutantDict] = {
'x__yield_complete_lines__mutmut_1': x__yield_complete_lines__mutmut_1, 
    'x__yield_complete_lines__mutmut_2': x__yield_complete_lines__mutmut_2, 
    'x__yield_complete_lines__mutmut_3': x__yield_complete_lines__mutmut_3, 
    'x__yield_complete_lines__mutmut_4': x__yield_complete_lines__mutmut_4, 
    'x__yield_complete_lines__mutmut_5': x__yield_complete_lines__mutmut_5, 
    'x__yield_complete_lines__mutmut_6': x__yield_complete_lines__mutmut_6, 
    'x__yield_complete_lines__mutmut_7': x__yield_complete_lines__mutmut_7, 
    'x__yield_complete_lines__mutmut_8': x__yield_complete_lines__mutmut_8, 
    'x__yield_complete_lines__mutmut_9': x__yield_complete_lines__mutmut_9, 
    'x__yield_complete_lines__mutmut_10': x__yield_complete_lines__mutmut_10, 
    'x__yield_complete_lines__mutmut_11': x__yield_complete_lines__mutmut_11
}

def _yield_complete_lines(*args, **kwargs):
    result = _mutmut_trampoline(x__yield_complete_lines__mutmut_orig, x__yield_complete_lines__mutmut_mutants, args, kwargs)
    return result 

_yield_complete_lines.__signature__ = _mutmut_signature(x__yield_complete_lines__mutmut_orig)
x__yield_complete_lines__mutmut_orig.__name__ = 'x__yield_complete_lines'


def x__yield_remaining_lines__mutmut_orig(buffer: str) -> Iterator[str]:
    """Yield any remaining lines from buffer."""
    for line in buffer.split("\n"):
        if line:
            yield line.rstrip()


def x__yield_remaining_lines__mutmut_1(buffer: str) -> Iterator[str]:
    """Yield any remaining lines from buffer."""
    for line in buffer.split(None):
        if line:
            yield line.rstrip()


def x__yield_remaining_lines__mutmut_2(buffer: str) -> Iterator[str]:
    """Yield any remaining lines from buffer."""
    for line in buffer.split("XX\nXX"):
        if line:
            yield line.rstrip()


def x__yield_remaining_lines__mutmut_3(buffer: str) -> Iterator[str]:
    """Yield any remaining lines from buffer."""
    for line in buffer.split("\n"):
        if line:
            yield line.lstrip()

x__yield_remaining_lines__mutmut_mutants : ClassVar[MutantDict] = {
'x__yield_remaining_lines__mutmut_1': x__yield_remaining_lines__mutmut_1, 
    'x__yield_remaining_lines__mutmut_2': x__yield_remaining_lines__mutmut_2, 
    'x__yield_remaining_lines__mutmut_3': x__yield_remaining_lines__mutmut_3
}

def _yield_remaining_lines(*args, **kwargs):
    result = _mutmut_trampoline(x__yield_remaining_lines__mutmut_orig, x__yield_remaining_lines__mutmut_mutants, args, kwargs)
    return result 

_yield_remaining_lines.__signature__ = _mutmut_signature(x__yield_remaining_lines__mutmut_orig)
x__yield_remaining_lines__mutmut_orig.__name__ = 'x__yield_remaining_lines'


def x__finalize_remaining_data__mutmut_orig(stdout: Any, buffer: str) -> Iterator[str]:
    """Read any remaining data and yield final lines."""
    remaining_data = stdout.read()
    if remaining_data:
        buffer += remaining_data

    yield from _yield_remaining_lines(buffer)


def x__finalize_remaining_data__mutmut_1(stdout: Any, buffer: str) -> Iterator[str]:
    """Read any remaining data and yield final lines."""
    remaining_data = None
    if remaining_data:
        buffer += remaining_data

    yield from _yield_remaining_lines(buffer)


def x__finalize_remaining_data__mutmut_2(stdout: Any, buffer: str) -> Iterator[str]:
    """Read any remaining data and yield final lines."""
    remaining_data = stdout.read()
    if remaining_data:
        buffer = remaining_data

    yield from _yield_remaining_lines(buffer)


def x__finalize_remaining_data__mutmut_3(stdout: Any, buffer: str) -> Iterator[str]:
    """Read any remaining data and yield final lines."""
    remaining_data = stdout.read()
    if remaining_data:
        buffer -= remaining_data

    yield from _yield_remaining_lines(buffer)


def x__finalize_remaining_data__mutmut_4(stdout: Any, buffer: str) -> Iterator[str]:
    """Read any remaining data and yield final lines."""
    remaining_data = stdout.read()
    if remaining_data:
        buffer += remaining_data

    yield from _yield_remaining_lines(None)

x__finalize_remaining_data__mutmut_mutants : ClassVar[MutantDict] = {
'x__finalize_remaining_data__mutmut_1': x__finalize_remaining_data__mutmut_1, 
    'x__finalize_remaining_data__mutmut_2': x__finalize_remaining_data__mutmut_2, 
    'x__finalize_remaining_data__mutmut_3': x__finalize_remaining_data__mutmut_3, 
    'x__finalize_remaining_data__mutmut_4': x__finalize_remaining_data__mutmut_4
}

def _finalize_remaining_data(*args, **kwargs):
    result = _mutmut_trampoline(x__finalize_remaining_data__mutmut_orig, x__finalize_remaining_data__mutmut_mutants, args, kwargs)
    return result 

_finalize_remaining_data.__signature__ = _mutmut_signature(x__finalize_remaining_data__mutmut_orig)
x__finalize_remaining_data__mutmut_orig.__name__ = 'x__finalize_remaining_data'


def x__stream_with_timeout__mutmut_orig(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_1(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_2(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = None
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_3(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(None)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_4(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = None
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_5(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = "XXXX"
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_6(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while False:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_7(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(None, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_8(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, None, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_9(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, None, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_10(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, None)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_11(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_12(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_13(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_14(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, )

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_15(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = None
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_16(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() + start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_17(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = None
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_18(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout + elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_19(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = None

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_20(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select(None, [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_21(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], None, [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_22(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], None, min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_23(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], None)

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_24(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_25(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_26(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_27(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], )

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_28(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(None, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_29(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, None))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_30(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_31(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, ))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_32(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(1.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_33(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = None
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_34(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(None, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_35(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, None)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_36(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_37(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, )
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_38(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                return

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_39(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(None):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_40(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = None
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_41(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            break


def x__stream_with_timeout__mutmut_42(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(None, buffer)
            break


def x__stream_with_timeout__mutmut_43(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, None)
            break


def x__stream_with_timeout__mutmut_44(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(buffer)
            break


def x__stream_with_timeout__mutmut_45(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, )
            break


def x__stream_with_timeout__mutmut_46(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
    """Stream output with timeout handling."""
    import select
    import time

    if not process.stdout:
        return

    start_time = time.time()
    _make_stdout_nonblocking(process.stdout)

    buffer = ""
    while True:
        _check_timeout_expired(start_time, timeout, cmd_str, process)

        # Use select with timeout
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        ready, _, _ = select.select([process.stdout], [], [], min(0.1, remaining))

        if ready:
            buffer, eof = _read_chunk_from_stdout(process.stdout, buffer)
            if eof:
                break

            # Yield complete lines
            for line, new_buffer in _yield_complete_lines(buffer):
                buffer = new_buffer
                yield line

        # Check if process ended
        if process.poll() is not None:
            yield from _finalize_remaining_data(process.stdout, buffer)
            return

x__stream_with_timeout__mutmut_mutants : ClassVar[MutantDict] = {
'x__stream_with_timeout__mutmut_1': x__stream_with_timeout__mutmut_1, 
    'x__stream_with_timeout__mutmut_2': x__stream_with_timeout__mutmut_2, 
    'x__stream_with_timeout__mutmut_3': x__stream_with_timeout__mutmut_3, 
    'x__stream_with_timeout__mutmut_4': x__stream_with_timeout__mutmut_4, 
    'x__stream_with_timeout__mutmut_5': x__stream_with_timeout__mutmut_5, 
    'x__stream_with_timeout__mutmut_6': x__stream_with_timeout__mutmut_6, 
    'x__stream_with_timeout__mutmut_7': x__stream_with_timeout__mutmut_7, 
    'x__stream_with_timeout__mutmut_8': x__stream_with_timeout__mutmut_8, 
    'x__stream_with_timeout__mutmut_9': x__stream_with_timeout__mutmut_9, 
    'x__stream_with_timeout__mutmut_10': x__stream_with_timeout__mutmut_10, 
    'x__stream_with_timeout__mutmut_11': x__stream_with_timeout__mutmut_11, 
    'x__stream_with_timeout__mutmut_12': x__stream_with_timeout__mutmut_12, 
    'x__stream_with_timeout__mutmut_13': x__stream_with_timeout__mutmut_13, 
    'x__stream_with_timeout__mutmut_14': x__stream_with_timeout__mutmut_14, 
    'x__stream_with_timeout__mutmut_15': x__stream_with_timeout__mutmut_15, 
    'x__stream_with_timeout__mutmut_16': x__stream_with_timeout__mutmut_16, 
    'x__stream_with_timeout__mutmut_17': x__stream_with_timeout__mutmut_17, 
    'x__stream_with_timeout__mutmut_18': x__stream_with_timeout__mutmut_18, 
    'x__stream_with_timeout__mutmut_19': x__stream_with_timeout__mutmut_19, 
    'x__stream_with_timeout__mutmut_20': x__stream_with_timeout__mutmut_20, 
    'x__stream_with_timeout__mutmut_21': x__stream_with_timeout__mutmut_21, 
    'x__stream_with_timeout__mutmut_22': x__stream_with_timeout__mutmut_22, 
    'x__stream_with_timeout__mutmut_23': x__stream_with_timeout__mutmut_23, 
    'x__stream_with_timeout__mutmut_24': x__stream_with_timeout__mutmut_24, 
    'x__stream_with_timeout__mutmut_25': x__stream_with_timeout__mutmut_25, 
    'x__stream_with_timeout__mutmut_26': x__stream_with_timeout__mutmut_26, 
    'x__stream_with_timeout__mutmut_27': x__stream_with_timeout__mutmut_27, 
    'x__stream_with_timeout__mutmut_28': x__stream_with_timeout__mutmut_28, 
    'x__stream_with_timeout__mutmut_29': x__stream_with_timeout__mutmut_29, 
    'x__stream_with_timeout__mutmut_30': x__stream_with_timeout__mutmut_30, 
    'x__stream_with_timeout__mutmut_31': x__stream_with_timeout__mutmut_31, 
    'x__stream_with_timeout__mutmut_32': x__stream_with_timeout__mutmut_32, 
    'x__stream_with_timeout__mutmut_33': x__stream_with_timeout__mutmut_33, 
    'x__stream_with_timeout__mutmut_34': x__stream_with_timeout__mutmut_34, 
    'x__stream_with_timeout__mutmut_35': x__stream_with_timeout__mutmut_35, 
    'x__stream_with_timeout__mutmut_36': x__stream_with_timeout__mutmut_36, 
    'x__stream_with_timeout__mutmut_37': x__stream_with_timeout__mutmut_37, 
    'x__stream_with_timeout__mutmut_38': x__stream_with_timeout__mutmut_38, 
    'x__stream_with_timeout__mutmut_39': x__stream_with_timeout__mutmut_39, 
    'x__stream_with_timeout__mutmut_40': x__stream_with_timeout__mutmut_40, 
    'x__stream_with_timeout__mutmut_41': x__stream_with_timeout__mutmut_41, 
    'x__stream_with_timeout__mutmut_42': x__stream_with_timeout__mutmut_42, 
    'x__stream_with_timeout__mutmut_43': x__stream_with_timeout__mutmut_43, 
    'x__stream_with_timeout__mutmut_44': x__stream_with_timeout__mutmut_44, 
    'x__stream_with_timeout__mutmut_45': x__stream_with_timeout__mutmut_45, 
    'x__stream_with_timeout__mutmut_46': x__stream_with_timeout__mutmut_46
}

def _stream_with_timeout(*args, **kwargs):
    result = _mutmut_trampoline(x__stream_with_timeout__mutmut_orig, x__stream_with_timeout__mutmut_mutants, args, kwargs)
    return result 

_stream_with_timeout.__signature__ = _mutmut_signature(x__stream_with_timeout__mutmut_orig)
x__stream_with_timeout__mutmut_orig.__name__ = 'x__stream_with_timeout'


def x__stream_without_timeout__mutmut_orig(process: Any) -> Iterator[str]:
    """Stream output without timeout (blocking I/O)."""
    if process.stdout:
        for line in process.stdout:
            yield line.rstrip()


def x__stream_without_timeout__mutmut_1(process: Any) -> Iterator[str]:
    """Stream output without timeout (blocking I/O)."""
    if process.stdout:
        for line in process.stdout:
            yield line.lstrip()

x__stream_without_timeout__mutmut_mutants : ClassVar[MutantDict] = {
'x__stream_without_timeout__mutmut_1': x__stream_without_timeout__mutmut_1
}

def _stream_without_timeout(*args, **kwargs):
    result = _mutmut_trampoline(x__stream_without_timeout__mutmut_orig, x__stream_without_timeout__mutmut_mutants, args, kwargs)
    return result 

_stream_without_timeout.__signature__ = _mutmut_signature(x__stream_without_timeout__mutmut_orig)
x__stream_without_timeout__mutmut_orig.__name__ = 'x__stream_without_timeout'


def x__cleanup_process__mutmut_orig(process: Any) -> None:
    """Ensure subprocess pipes are properly closed and process is terminated."""
    if process.stdout:
        process.stdout.close()
    if process.stderr:
        process.stderr.close()

    # Make sure process is terminated
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=1.0)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def x__cleanup_process__mutmut_1(process: Any) -> None:
    """Ensure subprocess pipes are properly closed and process is terminated."""
    if process.stdout:
        process.stdout.close()
    if process.stderr:
        process.stderr.close()

    # Make sure process is terminated
    if process.poll() is not None:
        process.terminate()
        try:
            process.wait(timeout=1.0)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def x__cleanup_process__mutmut_2(process: Any) -> None:
    """Ensure subprocess pipes are properly closed and process is terminated."""
    if process.stdout:
        process.stdout.close()
    if process.stderr:
        process.stderr.close()

    # Make sure process is terminated
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=None)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def x__cleanup_process__mutmut_3(process: Any) -> None:
    """Ensure subprocess pipes are properly closed and process is terminated."""
    if process.stdout:
        process.stdout.close()
    if process.stderr:
        process.stderr.close()

    # Make sure process is terminated
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=2.0)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()

x__cleanup_process__mutmut_mutants : ClassVar[MutantDict] = {
'x__cleanup_process__mutmut_1': x__cleanup_process__mutmut_1, 
    'x__cleanup_process__mutmut_2': x__cleanup_process__mutmut_2, 
    'x__cleanup_process__mutmut_3': x__cleanup_process__mutmut_3
}

def _cleanup_process(*args, **kwargs):
    result = _mutmut_trampoline(x__cleanup_process__mutmut_orig, x__cleanup_process__mutmut_mutants, args, kwargs)
    return result 

_cleanup_process.__signature__ = _mutmut_signature(x__cleanup_process__mutmut_orig)
x__cleanup_process__mutmut_orig.__name__ = 'x__cleanup_process'


def x_stream__mutmut_orig(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_1(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = True,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_2(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = None
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_3(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(None) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_4(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = "XX XX".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_5(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(None)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_6(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info(None, command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_7(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=None, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_8(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_9(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info(command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_10(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_11(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, )

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_12(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("XX🌊 Streaming commandXX", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_13(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_14(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 STREAMING COMMAND", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_15(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(None) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_16(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = None
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_17(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(None)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_18(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = None

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_19(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(None)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_20(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = None

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_21(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            None,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_22(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=None,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_23(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=None,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_24(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=None,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_25(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=None,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_26(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=None,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_27(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=None,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_28(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=None,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_29(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_30(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_31(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_32(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_33(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_34(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_35(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_36(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_37(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_38(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=False,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_39(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=2,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_40(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=False,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_41(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_42(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(None, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_43(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, None, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_44(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, None)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_45(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_46(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_47(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, )
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_48(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = None
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_49(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() and process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_50(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(None)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_51(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = None

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_52(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode == 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_53(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 1:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_54(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    None,
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_55(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code=None,
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_56(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=None,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_57(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=None,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_58(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_59(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_60(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_61(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_62(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="XXPROCESS_STREAM_FAILEDXX",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_63(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="process_stream_failed",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_64(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug(None, command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_65(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=None)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_66(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug(command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_67(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", )
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_68(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("XX✅ Stream completedXX", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_69(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_70(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ STREAM COMPLETED", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_71(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(None)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_72(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error(None, command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_73(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=None, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_74(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=None)
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_75(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error(command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_76(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_77(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, )
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_78(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("XX💥 Stream failedXX", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_79(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_80(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 STREAM FAILED", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_81(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(None))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_82(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            None,
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_83(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code=None,
            command=cmd_str,
        ) from e


def x_stream__mutmut_84(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=None,
        ) from e


def x_stream__mutmut_85(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
        ) from e


def x_stream__mutmut_86(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            command=cmd_str,
        ) from e


def x_stream__mutmut_87(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            ) from e


def x_stream__mutmut_88(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="XXPROCESS_STREAM_ERRORXX",
            command=cmd_str,
        ) from e


def x_stream__mutmut_89(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """Stream command output line by line.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to stream stderr (merged with stdout)
        **kwargs: Additional arguments passed to subprocess.Popen

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = prepare_environment(env)
    cwd = normalize_cwd(cwd)

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=run_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stream_stderr else subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            **kwargs,
        )

        try:
            if timeout is not None:
                yield from _stream_with_timeout(process, timeout, cmd_str)
                returncode = process.poll() or process.wait()
            else:
                yield from _stream_without_timeout(process)
                returncode = process.wait()

            if returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {returncode}: {cmd_str}",
                    code="PROCESS_STREAM_FAILED",
                    command=cmd_str,
                    return_code=returncode,
                )

            log.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise
        log.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="process_stream_error",
            command=cmd_str,
        ) from e

x_stream__mutmut_mutants : ClassVar[MutantDict] = {
'x_stream__mutmut_1': x_stream__mutmut_1, 
    'x_stream__mutmut_2': x_stream__mutmut_2, 
    'x_stream__mutmut_3': x_stream__mutmut_3, 
    'x_stream__mutmut_4': x_stream__mutmut_4, 
    'x_stream__mutmut_5': x_stream__mutmut_5, 
    'x_stream__mutmut_6': x_stream__mutmut_6, 
    'x_stream__mutmut_7': x_stream__mutmut_7, 
    'x_stream__mutmut_8': x_stream__mutmut_8, 
    'x_stream__mutmut_9': x_stream__mutmut_9, 
    'x_stream__mutmut_10': x_stream__mutmut_10, 
    'x_stream__mutmut_11': x_stream__mutmut_11, 
    'x_stream__mutmut_12': x_stream__mutmut_12, 
    'x_stream__mutmut_13': x_stream__mutmut_13, 
    'x_stream__mutmut_14': x_stream__mutmut_14, 
    'x_stream__mutmut_15': x_stream__mutmut_15, 
    'x_stream__mutmut_16': x_stream__mutmut_16, 
    'x_stream__mutmut_17': x_stream__mutmut_17, 
    'x_stream__mutmut_18': x_stream__mutmut_18, 
    'x_stream__mutmut_19': x_stream__mutmut_19, 
    'x_stream__mutmut_20': x_stream__mutmut_20, 
    'x_stream__mutmut_21': x_stream__mutmut_21, 
    'x_stream__mutmut_22': x_stream__mutmut_22, 
    'x_stream__mutmut_23': x_stream__mutmut_23, 
    'x_stream__mutmut_24': x_stream__mutmut_24, 
    'x_stream__mutmut_25': x_stream__mutmut_25, 
    'x_stream__mutmut_26': x_stream__mutmut_26, 
    'x_stream__mutmut_27': x_stream__mutmut_27, 
    'x_stream__mutmut_28': x_stream__mutmut_28, 
    'x_stream__mutmut_29': x_stream__mutmut_29, 
    'x_stream__mutmut_30': x_stream__mutmut_30, 
    'x_stream__mutmut_31': x_stream__mutmut_31, 
    'x_stream__mutmut_32': x_stream__mutmut_32, 
    'x_stream__mutmut_33': x_stream__mutmut_33, 
    'x_stream__mutmut_34': x_stream__mutmut_34, 
    'x_stream__mutmut_35': x_stream__mutmut_35, 
    'x_stream__mutmut_36': x_stream__mutmut_36, 
    'x_stream__mutmut_37': x_stream__mutmut_37, 
    'x_stream__mutmut_38': x_stream__mutmut_38, 
    'x_stream__mutmut_39': x_stream__mutmut_39, 
    'x_stream__mutmut_40': x_stream__mutmut_40, 
    'x_stream__mutmut_41': x_stream__mutmut_41, 
    'x_stream__mutmut_42': x_stream__mutmut_42, 
    'x_stream__mutmut_43': x_stream__mutmut_43, 
    'x_stream__mutmut_44': x_stream__mutmut_44, 
    'x_stream__mutmut_45': x_stream__mutmut_45, 
    'x_stream__mutmut_46': x_stream__mutmut_46, 
    'x_stream__mutmut_47': x_stream__mutmut_47, 
    'x_stream__mutmut_48': x_stream__mutmut_48, 
    'x_stream__mutmut_49': x_stream__mutmut_49, 
    'x_stream__mutmut_50': x_stream__mutmut_50, 
    'x_stream__mutmut_51': x_stream__mutmut_51, 
    'x_stream__mutmut_52': x_stream__mutmut_52, 
    'x_stream__mutmut_53': x_stream__mutmut_53, 
    'x_stream__mutmut_54': x_stream__mutmut_54, 
    'x_stream__mutmut_55': x_stream__mutmut_55, 
    'x_stream__mutmut_56': x_stream__mutmut_56, 
    'x_stream__mutmut_57': x_stream__mutmut_57, 
    'x_stream__mutmut_58': x_stream__mutmut_58, 
    'x_stream__mutmut_59': x_stream__mutmut_59, 
    'x_stream__mutmut_60': x_stream__mutmut_60, 
    'x_stream__mutmut_61': x_stream__mutmut_61, 
    'x_stream__mutmut_62': x_stream__mutmut_62, 
    'x_stream__mutmut_63': x_stream__mutmut_63, 
    'x_stream__mutmut_64': x_stream__mutmut_64, 
    'x_stream__mutmut_65': x_stream__mutmut_65, 
    'x_stream__mutmut_66': x_stream__mutmut_66, 
    'x_stream__mutmut_67': x_stream__mutmut_67, 
    'x_stream__mutmut_68': x_stream__mutmut_68, 
    'x_stream__mutmut_69': x_stream__mutmut_69, 
    'x_stream__mutmut_70': x_stream__mutmut_70, 
    'x_stream__mutmut_71': x_stream__mutmut_71, 
    'x_stream__mutmut_72': x_stream__mutmut_72, 
    'x_stream__mutmut_73': x_stream__mutmut_73, 
    'x_stream__mutmut_74': x_stream__mutmut_74, 
    'x_stream__mutmut_75': x_stream__mutmut_75, 
    'x_stream__mutmut_76': x_stream__mutmut_76, 
    'x_stream__mutmut_77': x_stream__mutmut_77, 
    'x_stream__mutmut_78': x_stream__mutmut_78, 
    'x_stream__mutmut_79': x_stream__mutmut_79, 
    'x_stream__mutmut_80': x_stream__mutmut_80, 
    'x_stream__mutmut_81': x_stream__mutmut_81, 
    'x_stream__mutmut_82': x_stream__mutmut_82, 
    'x_stream__mutmut_83': x_stream__mutmut_83, 
    'x_stream__mutmut_84': x_stream__mutmut_84, 
    'x_stream__mutmut_85': x_stream__mutmut_85, 
    'x_stream__mutmut_86': x_stream__mutmut_86, 
    'x_stream__mutmut_87': x_stream__mutmut_87, 
    'x_stream__mutmut_88': x_stream__mutmut_88, 
    'x_stream__mutmut_89': x_stream__mutmut_89
}

def stream(*args, **kwargs):
    result = _mutmut_trampoline(x_stream__mutmut_orig, x_stream__mutmut_mutants, args, kwargs)
    return result 

stream.__signature__ = _mutmut_signature(x_stream__mutmut_orig)
x_stream__mutmut_orig.__name__ = 'x_stream'


# <3 🧱🤝🏃🪄
