# provide/foundation/process/aio/execution.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio
import builtins
from collections.abc import Mapping
import contextlib
from pathlib import Path
from typing import Any

from provide.foundation.errors.config import ValidationError
from provide.foundation.errors.process import ProcessError, ProcessTimeoutError
from provide.foundation.logger import get_logger
from provide.foundation.process.shared import (
    CompletedProcess,
    filter_subprocess_kwargs,
    prepare_environment,
)

"""Core async subprocess execution."""

log = get_logger(__name__)
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


async def x_create_subprocess__mutmut_orig(
    cmd: list[str] | str,
    cmd_str: str,
    shell: bool,
    cwd: str | None,
    run_env: dict[str, str],
    capture_output: bool,
    input: bytes | None,
    kwargs: dict[str, Any],
) -> asyncio.subprocess.Process:
    """Create an async subprocess.

    Args:
        cmd: Command to execute
        cmd_str: String representation of command
        shell: Whether to use shell execution
        cwd: Working directory
        run_env: Environment variables
        capture_output: Whether to capture stdout/stderr
        input: Input bytes for stdin
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    common_args = {
        "cwd": cwd,
        "env": run_env,
        "stdout": asyncio.subprocess.PIPE if capture_output else None,
        "stderr": asyncio.subprocess.PIPE if capture_output else None,
        "stdin": asyncio.subprocess.PIPE if input else None,
        **filter_subprocess_kwargs(kwargs),
    }

    if shell:
        return await asyncio.create_subprocess_shell(cmd_str, **common_args)
    else:
        return await asyncio.create_subprocess_exec(*(cmd if isinstance(cmd, list) else [cmd]), **common_args)


async def x_create_subprocess__mutmut_1(
    cmd: list[str] | str,
    cmd_str: str,
    shell: bool,
    cwd: str | None,
    run_env: dict[str, str],
    capture_output: bool,
    input: bytes | None,
    kwargs: dict[str, Any],
) -> asyncio.subprocess.Process:
    """Create an async subprocess.

    Args:
        cmd: Command to execute
        cmd_str: String representation of command
        shell: Whether to use shell execution
        cwd: Working directory
        run_env: Environment variables
        capture_output: Whether to capture stdout/stderr
        input: Input bytes for stdin
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    common_args = None

    if shell:
        return await asyncio.create_subprocess_shell(cmd_str, **common_args)
    else:
        return await asyncio.create_subprocess_exec(*(cmd if isinstance(cmd, list) else [cmd]), **common_args)


async def x_create_subprocess__mutmut_2(
    cmd: list[str] | str,
    cmd_str: str,
    shell: bool,
    cwd: str | None,
    run_env: dict[str, str],
    capture_output: bool,
    input: bytes | None,
    kwargs: dict[str, Any],
) -> asyncio.subprocess.Process:
    """Create an async subprocess.

    Args:
        cmd: Command to execute
        cmd_str: String representation of command
        shell: Whether to use shell execution
        cwd: Working directory
        run_env: Environment variables
        capture_output: Whether to capture stdout/stderr
        input: Input bytes for stdin
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    common_args = {
        "XXcwdXX": cwd,
        "env": run_env,
        "stdout": asyncio.subprocess.PIPE if capture_output else None,
        "stderr": asyncio.subprocess.PIPE if capture_output else None,
        "stdin": asyncio.subprocess.PIPE if input else None,
        **filter_subprocess_kwargs(kwargs),
    }

    if shell:
        return await asyncio.create_subprocess_shell(cmd_str, **common_args)
    else:
        return await asyncio.create_subprocess_exec(*(cmd if isinstance(cmd, list) else [cmd]), **common_args)


async def x_create_subprocess__mutmut_3(
    cmd: list[str] | str,
    cmd_str: str,
    shell: bool,
    cwd: str | None,
    run_env: dict[str, str],
    capture_output: bool,
    input: bytes | None,
    kwargs: dict[str, Any],
) -> asyncio.subprocess.Process:
    """Create an async subprocess.

    Args:
        cmd: Command to execute
        cmd_str: String representation of command
        shell: Whether to use shell execution
        cwd: Working directory
        run_env: Environment variables
        capture_output: Whether to capture stdout/stderr
        input: Input bytes for stdin
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    common_args = {
        "CWD": cwd,
        "env": run_env,
        "stdout": asyncio.subprocess.PIPE if capture_output else None,
        "stderr": asyncio.subprocess.PIPE if capture_output else None,
        "stdin": asyncio.subprocess.PIPE if input else None,
        **filter_subprocess_kwargs(kwargs),
    }

    if shell:
        return await asyncio.create_subprocess_shell(cmd_str, **common_args)
    else:
        return await asyncio.create_subprocess_exec(*(cmd if isinstance(cmd, list) else [cmd]), **common_args)


async def x_create_subprocess__mutmut_4(
    cmd: list[str] | str,
    cmd_str: str,
    shell: bool,
    cwd: str | None,
    run_env: dict[str, str],
    capture_output: bool,
    input: bytes | None,
    kwargs: dict[str, Any],
) -> asyncio.subprocess.Process:
    """Create an async subprocess.

    Args:
        cmd: Command to execute
        cmd_str: String representation of command
        shell: Whether to use shell execution
        cwd: Working directory
        run_env: Environment variables
        capture_output: Whether to capture stdout/stderr
        input: Input bytes for stdin
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    common_args = {
        "cwd": cwd,
        "XXenvXX": run_env,
        "stdout": asyncio.subprocess.PIPE if capture_output else None,
        "stderr": asyncio.subprocess.PIPE if capture_output else None,
        "stdin": asyncio.subprocess.PIPE if input else None,
        **filter_subprocess_kwargs(kwargs),
    }

    if shell:
        return await asyncio.create_subprocess_shell(cmd_str, **common_args)
    else:
        return await asyncio.create_subprocess_exec(*(cmd if isinstance(cmd, list) else [cmd]), **common_args)


async def x_create_subprocess__mutmut_5(
    cmd: list[str] | str,
    cmd_str: str,
    shell: bool,
    cwd: str | None,
    run_env: dict[str, str],
    capture_output: bool,
    input: bytes | None,
    kwargs: dict[str, Any],
) -> asyncio.subprocess.Process:
    """Create an async subprocess.

    Args:
        cmd: Command to execute
        cmd_str: String representation of command
        shell: Whether to use shell execution
        cwd: Working directory
        run_env: Environment variables
        capture_output: Whether to capture stdout/stderr
        input: Input bytes for stdin
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    common_args = {
        "cwd": cwd,
        "ENV": run_env,
        "stdout": asyncio.subprocess.PIPE if capture_output else None,
        "stderr": asyncio.subprocess.PIPE if capture_output else None,
        "stdin": asyncio.subprocess.PIPE if input else None,
        **filter_subprocess_kwargs(kwargs),
    }

    if shell:
        return await asyncio.create_subprocess_shell(cmd_str, **common_args)
    else:
        return await asyncio.create_subprocess_exec(*(cmd if isinstance(cmd, list) else [cmd]), **common_args)


async def x_create_subprocess__mutmut_6(
    cmd: list[str] | str,
    cmd_str: str,
    shell: bool,
    cwd: str | None,
    run_env: dict[str, str],
    capture_output: bool,
    input: bytes | None,
    kwargs: dict[str, Any],
) -> asyncio.subprocess.Process:
    """Create an async subprocess.

    Args:
        cmd: Command to execute
        cmd_str: String representation of command
        shell: Whether to use shell execution
        cwd: Working directory
        run_env: Environment variables
        capture_output: Whether to capture stdout/stderr
        input: Input bytes for stdin
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    common_args = {
        "cwd": cwd,
        "env": run_env,
        "XXstdoutXX": asyncio.subprocess.PIPE if capture_output else None,
        "stderr": asyncio.subprocess.PIPE if capture_output else None,
        "stdin": asyncio.subprocess.PIPE if input else None,
        **filter_subprocess_kwargs(kwargs),
    }

    if shell:
        return await asyncio.create_subprocess_shell(cmd_str, **common_args)
    else:
        return await asyncio.create_subprocess_exec(*(cmd if isinstance(cmd, list) else [cmd]), **common_args)


async def x_create_subprocess__mutmut_7(
    cmd: list[str] | str,
    cmd_str: str,
    shell: bool,
    cwd: str | None,
    run_env: dict[str, str],
    capture_output: bool,
    input: bytes | None,
    kwargs: dict[str, Any],
) -> asyncio.subprocess.Process:
    """Create an async subprocess.

    Args:
        cmd: Command to execute
        cmd_str: String representation of command
        shell: Whether to use shell execution
        cwd: Working directory
        run_env: Environment variables
        capture_output: Whether to capture stdout/stderr
        input: Input bytes for stdin
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    common_args = {
        "cwd": cwd,
        "env": run_env,
        "STDOUT": asyncio.subprocess.PIPE if capture_output else None,
        "stderr": asyncio.subprocess.PIPE if capture_output else None,
        "stdin": asyncio.subprocess.PIPE if input else None,
        **filter_subprocess_kwargs(kwargs),
    }

    if shell:
        return await asyncio.create_subprocess_shell(cmd_str, **common_args)
    else:
        return await asyncio.create_subprocess_exec(*(cmd if isinstance(cmd, list) else [cmd]), **common_args)


async def x_create_subprocess__mutmut_8(
    cmd: list[str] | str,
    cmd_str: str,
    shell: bool,
    cwd: str | None,
    run_env: dict[str, str],
    capture_output: bool,
    input: bytes | None,
    kwargs: dict[str, Any],
) -> asyncio.subprocess.Process:
    """Create an async subprocess.

    Args:
        cmd: Command to execute
        cmd_str: String representation of command
        shell: Whether to use shell execution
        cwd: Working directory
        run_env: Environment variables
        capture_output: Whether to capture stdout/stderr
        input: Input bytes for stdin
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    common_args = {
        "cwd": cwd,
        "env": run_env,
        "stdout": asyncio.subprocess.PIPE if capture_output else None,
        "XXstderrXX": asyncio.subprocess.PIPE if capture_output else None,
        "stdin": asyncio.subprocess.PIPE if input else None,
        **filter_subprocess_kwargs(kwargs),
    }

    if shell:
        return await asyncio.create_subprocess_shell(cmd_str, **common_args)
    else:
        return await asyncio.create_subprocess_exec(*(cmd if isinstance(cmd, list) else [cmd]), **common_args)


async def x_create_subprocess__mutmut_9(
    cmd: list[str] | str,
    cmd_str: str,
    shell: bool,
    cwd: str | None,
    run_env: dict[str, str],
    capture_output: bool,
    input: bytes | None,
    kwargs: dict[str, Any],
) -> asyncio.subprocess.Process:
    """Create an async subprocess.

    Args:
        cmd: Command to execute
        cmd_str: String representation of command
        shell: Whether to use shell execution
        cwd: Working directory
        run_env: Environment variables
        capture_output: Whether to capture stdout/stderr
        input: Input bytes for stdin
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    common_args = {
        "cwd": cwd,
        "env": run_env,
        "stdout": asyncio.subprocess.PIPE if capture_output else None,
        "STDERR": asyncio.subprocess.PIPE if capture_output else None,
        "stdin": asyncio.subprocess.PIPE if input else None,
        **filter_subprocess_kwargs(kwargs),
    }

    if shell:
        return await asyncio.create_subprocess_shell(cmd_str, **common_args)
    else:
        return await asyncio.create_subprocess_exec(*(cmd if isinstance(cmd, list) else [cmd]), **common_args)


async def x_create_subprocess__mutmut_10(
    cmd: list[str] | str,
    cmd_str: str,
    shell: bool,
    cwd: str | None,
    run_env: dict[str, str],
    capture_output: bool,
    input: bytes | None,
    kwargs: dict[str, Any],
) -> asyncio.subprocess.Process:
    """Create an async subprocess.

    Args:
        cmd: Command to execute
        cmd_str: String representation of command
        shell: Whether to use shell execution
        cwd: Working directory
        run_env: Environment variables
        capture_output: Whether to capture stdout/stderr
        input: Input bytes for stdin
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    common_args = {
        "cwd": cwd,
        "env": run_env,
        "stdout": asyncio.subprocess.PIPE if capture_output else None,
        "stderr": asyncio.subprocess.PIPE if capture_output else None,
        "XXstdinXX": asyncio.subprocess.PIPE if input else None,
        **filter_subprocess_kwargs(kwargs),
    }

    if shell:
        return await asyncio.create_subprocess_shell(cmd_str, **common_args)
    else:
        return await asyncio.create_subprocess_exec(*(cmd if isinstance(cmd, list) else [cmd]), **common_args)


async def x_create_subprocess__mutmut_11(
    cmd: list[str] | str,
    cmd_str: str,
    shell: bool,
    cwd: str | None,
    run_env: dict[str, str],
    capture_output: bool,
    input: bytes | None,
    kwargs: dict[str, Any],
) -> asyncio.subprocess.Process:
    """Create an async subprocess.

    Args:
        cmd: Command to execute
        cmd_str: String representation of command
        shell: Whether to use shell execution
        cwd: Working directory
        run_env: Environment variables
        capture_output: Whether to capture stdout/stderr
        input: Input bytes for stdin
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    common_args = {
        "cwd": cwd,
        "env": run_env,
        "stdout": asyncio.subprocess.PIPE if capture_output else None,
        "stderr": asyncio.subprocess.PIPE if capture_output else None,
        "STDIN": asyncio.subprocess.PIPE if input else None,
        **filter_subprocess_kwargs(kwargs),
    }

    if shell:
        return await asyncio.create_subprocess_shell(cmd_str, **common_args)
    else:
        return await asyncio.create_subprocess_exec(*(cmd if isinstance(cmd, list) else [cmd]), **common_args)


async def x_create_subprocess__mutmut_12(
    cmd: list[str] | str,
    cmd_str: str,
    shell: bool,
    cwd: str | None,
    run_env: dict[str, str],
    capture_output: bool,
    input: bytes | None,
    kwargs: dict[str, Any],
) -> asyncio.subprocess.Process:
    """Create an async subprocess.

    Args:
        cmd: Command to execute
        cmd_str: String representation of command
        shell: Whether to use shell execution
        cwd: Working directory
        run_env: Environment variables
        capture_output: Whether to capture stdout/stderr
        input: Input bytes for stdin
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    common_args = {
        "cwd": cwd,
        "env": run_env,
        "stdout": asyncio.subprocess.PIPE if capture_output else None,
        "stderr": asyncio.subprocess.PIPE if capture_output else None,
        "stdin": asyncio.subprocess.PIPE if input else None,
        **filter_subprocess_kwargs(None),
    }

    if shell:
        return await asyncio.create_subprocess_shell(cmd_str, **common_args)
    else:
        return await asyncio.create_subprocess_exec(*(cmd if isinstance(cmd, list) else [cmd]), **common_args)


async def x_create_subprocess__mutmut_13(
    cmd: list[str] | str,
    cmd_str: str,
    shell: bool,
    cwd: str | None,
    run_env: dict[str, str],
    capture_output: bool,
    input: bytes | None,
    kwargs: dict[str, Any],
) -> asyncio.subprocess.Process:
    """Create an async subprocess.

    Args:
        cmd: Command to execute
        cmd_str: String representation of command
        shell: Whether to use shell execution
        cwd: Working directory
        run_env: Environment variables
        capture_output: Whether to capture stdout/stderr
        input: Input bytes for stdin
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    common_args = {
        "cwd": cwd,
        "env": run_env,
        "stdout": asyncio.subprocess.PIPE if capture_output else None,
        "stderr": asyncio.subprocess.PIPE if capture_output else None,
        "stdin": asyncio.subprocess.PIPE if input else None,
        **filter_subprocess_kwargs(kwargs),
    }

    if shell:
        return await asyncio.create_subprocess_shell(None, **common_args)
    else:
        return await asyncio.create_subprocess_exec(*(cmd if isinstance(cmd, list) else [cmd]), **common_args)


async def x_create_subprocess__mutmut_14(
    cmd: list[str] | str,
    cmd_str: str,
    shell: bool,
    cwd: str | None,
    run_env: dict[str, str],
    capture_output: bool,
    input: bytes | None,
    kwargs: dict[str, Any],
) -> asyncio.subprocess.Process:
    """Create an async subprocess.

    Args:
        cmd: Command to execute
        cmd_str: String representation of command
        shell: Whether to use shell execution
        cwd: Working directory
        run_env: Environment variables
        capture_output: Whether to capture stdout/stderr
        input: Input bytes for stdin
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    common_args = {
        "cwd": cwd,
        "env": run_env,
        "stdout": asyncio.subprocess.PIPE if capture_output else None,
        "stderr": asyncio.subprocess.PIPE if capture_output else None,
        "stdin": asyncio.subprocess.PIPE if input else None,
        **filter_subprocess_kwargs(kwargs),
    }

    if shell:
        return await asyncio.create_subprocess_shell(**common_args)
    else:
        return await asyncio.create_subprocess_exec(*(cmd if isinstance(cmd, list) else [cmd]), **common_args)


async def x_create_subprocess__mutmut_15(
    cmd: list[str] | str,
    cmd_str: str,
    shell: bool,
    cwd: str | None,
    run_env: dict[str, str],
    capture_output: bool,
    input: bytes | None,
    kwargs: dict[str, Any],
) -> asyncio.subprocess.Process:
    """Create an async subprocess.

    Args:
        cmd: Command to execute
        cmd_str: String representation of command
        shell: Whether to use shell execution
        cwd: Working directory
        run_env: Environment variables
        capture_output: Whether to capture stdout/stderr
        input: Input bytes for stdin
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    common_args = {
        "cwd": cwd,
        "env": run_env,
        "stdout": asyncio.subprocess.PIPE if capture_output else None,
        "stderr": asyncio.subprocess.PIPE if capture_output else None,
        "stdin": asyncio.subprocess.PIPE if input else None,
        **filter_subprocess_kwargs(kwargs),
    }

    if shell:
        return await asyncio.create_subprocess_shell(
            cmd_str,
        )
    else:
        return await asyncio.create_subprocess_exec(*(cmd if isinstance(cmd, list) else [cmd]), **common_args)


async def x_create_subprocess__mutmut_16(
    cmd: list[str] | str,
    cmd_str: str,
    shell: bool,
    cwd: str | None,
    run_env: dict[str, str],
    capture_output: bool,
    input: bytes | None,
    kwargs: dict[str, Any],
) -> asyncio.subprocess.Process:
    """Create an async subprocess.

    Args:
        cmd: Command to execute
        cmd_str: String representation of command
        shell: Whether to use shell execution
        cwd: Working directory
        run_env: Environment variables
        capture_output: Whether to capture stdout/stderr
        input: Input bytes for stdin
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    common_args = {
        "cwd": cwd,
        "env": run_env,
        "stdout": asyncio.subprocess.PIPE if capture_output else None,
        "stderr": asyncio.subprocess.PIPE if capture_output else None,
        "stdin": asyncio.subprocess.PIPE if input else None,
        **filter_subprocess_kwargs(kwargs),
    }

    if shell:
        return await asyncio.create_subprocess_shell(cmd_str, **common_args)
    else:
        return await asyncio.create_subprocess_exec(**common_args)


async def x_create_subprocess__mutmut_17(
    cmd: list[str] | str,
    cmd_str: str,
    shell: bool,
    cwd: str | None,
    run_env: dict[str, str],
    capture_output: bool,
    input: bytes | None,
    kwargs: dict[str, Any],
) -> asyncio.subprocess.Process:
    """Create an async subprocess.

    Args:
        cmd: Command to execute
        cmd_str: String representation of command
        shell: Whether to use shell execution
        cwd: Working directory
        run_env: Environment variables
        capture_output: Whether to capture stdout/stderr
        input: Input bytes for stdin
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    common_args = {
        "cwd": cwd,
        "env": run_env,
        "stdout": asyncio.subprocess.PIPE if capture_output else None,
        "stderr": asyncio.subprocess.PIPE if capture_output else None,
        "stdin": asyncio.subprocess.PIPE if input else None,
        **filter_subprocess_kwargs(kwargs),
    }

    if shell:
        return await asyncio.create_subprocess_shell(cmd_str, **common_args)
    else:
        return await asyncio.create_subprocess_exec(
            *(cmd if isinstance(cmd, list) else [cmd]),
        )


x_create_subprocess__mutmut_mutants: ClassVar[MutantDict] = {
    "x_create_subprocess__mutmut_1": x_create_subprocess__mutmut_1,
    "x_create_subprocess__mutmut_2": x_create_subprocess__mutmut_2,
    "x_create_subprocess__mutmut_3": x_create_subprocess__mutmut_3,
    "x_create_subprocess__mutmut_4": x_create_subprocess__mutmut_4,
    "x_create_subprocess__mutmut_5": x_create_subprocess__mutmut_5,
    "x_create_subprocess__mutmut_6": x_create_subprocess__mutmut_6,
    "x_create_subprocess__mutmut_7": x_create_subprocess__mutmut_7,
    "x_create_subprocess__mutmut_8": x_create_subprocess__mutmut_8,
    "x_create_subprocess__mutmut_9": x_create_subprocess__mutmut_9,
    "x_create_subprocess__mutmut_10": x_create_subprocess__mutmut_10,
    "x_create_subprocess__mutmut_11": x_create_subprocess__mutmut_11,
    "x_create_subprocess__mutmut_12": x_create_subprocess__mutmut_12,
    "x_create_subprocess__mutmut_13": x_create_subprocess__mutmut_13,
    "x_create_subprocess__mutmut_14": x_create_subprocess__mutmut_14,
    "x_create_subprocess__mutmut_15": x_create_subprocess__mutmut_15,
    "x_create_subprocess__mutmut_16": x_create_subprocess__mutmut_16,
    "x_create_subprocess__mutmut_17": x_create_subprocess__mutmut_17,
}


def create_subprocess(*args, **kwargs):
    result = _mutmut_trampoline(
        x_create_subprocess__mutmut_orig, x_create_subprocess__mutmut_mutants, args, kwargs
    )
    return result


create_subprocess.__signature__ = _mutmut_signature(x_create_subprocess__mutmut_orig)
x_create_subprocess__mutmut_orig.__name__ = "x_create_subprocess"


async def x_read_stream_continuously__mutmut_orig(
    stream: asyncio.StreamReader | None,
) -> bytes:
    """Continuously read from a stream until EOF.

    Args:
        stream: Stream to read from

    Returns:
        All bytes read from stream
    """
    if stream is None:
        return b""

    chunks: list[bytes] = []
    try:
        while True:
            chunk = await stream.read(8192)  # Read in 8KB chunks
            if not chunk:
                break
            chunks.append(chunk)
    except (asyncio.CancelledError, OSError, EOFError, ValueError):
        # Stream closed or error, return what we have
        # OSError: stream/file errors
        # EOFError: end of stream
        # ValueError: invalid stream state
        # CancelledError: task cancelled
        pass
    return b"".join(chunks)


async def x_read_stream_continuously__mutmut_1(
    stream: asyncio.StreamReader | None,
) -> bytes:
    """Continuously read from a stream until EOF.

    Args:
        stream: Stream to read from

    Returns:
        All bytes read from stream
    """
    if stream is not None:
        return b""

    chunks: list[bytes] = []
    try:
        while True:
            chunk = await stream.read(8192)  # Read in 8KB chunks
            if not chunk:
                break
            chunks.append(chunk)
    except (asyncio.CancelledError, OSError, EOFError, ValueError):
        # Stream closed or error, return what we have
        # OSError: stream/file errors
        # EOFError: end of stream
        # ValueError: invalid stream state
        # CancelledError: task cancelled
        pass
    return b"".join(chunks)


async def x_read_stream_continuously__mutmut_2(
    stream: asyncio.StreamReader | None,
) -> bytes:
    """Continuously read from a stream until EOF.

    Args:
        stream: Stream to read from

    Returns:
        All bytes read from stream
    """
    if stream is None:
        return b"XXXX"

    chunks: list[bytes] = []
    try:
        while True:
            chunk = await stream.read(8192)  # Read in 8KB chunks
            if not chunk:
                break
            chunks.append(chunk)
    except (asyncio.CancelledError, OSError, EOFError, ValueError):
        # Stream closed or error, return what we have
        # OSError: stream/file errors
        # EOFError: end of stream
        # ValueError: invalid stream state
        # CancelledError: task cancelled
        pass
    return b"".join(chunks)


async def x_read_stream_continuously__mutmut_3(
    stream: asyncio.StreamReader | None,
) -> bytes:
    """Continuously read from a stream until EOF.

    Args:
        stream: Stream to read from

    Returns:
        All bytes read from stream
    """
    if stream is None:
        return b""

    chunks: list[bytes] = []
    try:
        while True:
            chunk = await stream.read(8192)  # Read in 8KB chunks
            if not chunk:
                break
            chunks.append(chunk)
    except (asyncio.CancelledError, OSError, EOFError, ValueError):
        # Stream closed or error, return what we have
        # OSError: stream/file errors
        # EOFError: end of stream
        # ValueError: invalid stream state
        # CancelledError: task cancelled
        pass
    return b"".join(chunks)


async def x_read_stream_continuously__mutmut_4(
    stream: asyncio.StreamReader | None,
) -> bytes:
    """Continuously read from a stream until EOF.

    Args:
        stream: Stream to read from

    Returns:
        All bytes read from stream
    """
    if stream is None:
        return b""

    chunks: list[bytes] = []
    try:
        while True:
            chunk = await stream.read(8192)  # Read in 8KB chunks
            if not chunk:
                break
            chunks.append(chunk)
    except (asyncio.CancelledError, OSError, EOFError, ValueError):
        # Stream closed or error, return what we have
        # OSError: stream/file errors
        # EOFError: end of stream
        # ValueError: invalid stream state
        # CancelledError: task cancelled
        pass
    return b"".join(chunks)


async def x_read_stream_continuously__mutmut_5(
    stream: asyncio.StreamReader | None,
) -> bytes:
    """Continuously read from a stream until EOF.

    Args:
        stream: Stream to read from

    Returns:
        All bytes read from stream
    """
    if stream is None:
        return b""

    chunks: list[bytes] = None
    try:
        while True:
            chunk = await stream.read(8192)  # Read in 8KB chunks
            if not chunk:
                break
            chunks.append(chunk)
    except (asyncio.CancelledError, OSError, EOFError, ValueError):
        # Stream closed or error, return what we have
        # OSError: stream/file errors
        # EOFError: end of stream
        # ValueError: invalid stream state
        # CancelledError: task cancelled
        pass
    return b"".join(chunks)


async def x_read_stream_continuously__mutmut_6(
    stream: asyncio.StreamReader | None,
) -> bytes:
    """Continuously read from a stream until EOF.

    Args:
        stream: Stream to read from

    Returns:
        All bytes read from stream
    """
    if stream is None:
        return b""

    chunks: list[bytes] = []
    try:
        while False:
            chunk = await stream.read(8192)  # Read in 8KB chunks
            if not chunk:
                break
            chunks.append(chunk)
    except (asyncio.CancelledError, OSError, EOFError, ValueError):
        # Stream closed or error, return what we have
        # OSError: stream/file errors
        # EOFError: end of stream
        # ValueError: invalid stream state
        # CancelledError: task cancelled
        pass
    return b"".join(chunks)


async def x_read_stream_continuously__mutmut_7(
    stream: asyncio.StreamReader | None,
) -> bytes:
    """Continuously read from a stream until EOF.

    Args:
        stream: Stream to read from

    Returns:
        All bytes read from stream
    """
    if stream is None:
        return b""

    chunks: list[bytes] = []
    try:
        while True:
            chunk = None  # Read in 8KB chunks
            if not chunk:
                break
            chunks.append(chunk)
    except (asyncio.CancelledError, OSError, EOFError, ValueError):
        # Stream closed or error, return what we have
        # OSError: stream/file errors
        # EOFError: end of stream
        # ValueError: invalid stream state
        # CancelledError: task cancelled
        pass
    return b"".join(chunks)


async def x_read_stream_continuously__mutmut_8(
    stream: asyncio.StreamReader | None,
) -> bytes:
    """Continuously read from a stream until EOF.

    Args:
        stream: Stream to read from

    Returns:
        All bytes read from stream
    """
    if stream is None:
        return b""

    chunks: list[bytes] = []
    try:
        while True:
            chunk = await stream.read(None)  # Read in 8KB chunks
            if not chunk:
                break
            chunks.append(chunk)
    except (asyncio.CancelledError, OSError, EOFError, ValueError):
        # Stream closed or error, return what we have
        # OSError: stream/file errors
        # EOFError: end of stream
        # ValueError: invalid stream state
        # CancelledError: task cancelled
        pass
    return b"".join(chunks)


async def x_read_stream_continuously__mutmut_9(
    stream: asyncio.StreamReader | None,
) -> bytes:
    """Continuously read from a stream until EOF.

    Args:
        stream: Stream to read from

    Returns:
        All bytes read from stream
    """
    if stream is None:
        return b""

    chunks: list[bytes] = []
    try:
        while True:
            chunk = await stream.read(8193)  # Read in 8KB chunks
            if not chunk:
                break
            chunks.append(chunk)
    except (asyncio.CancelledError, OSError, EOFError, ValueError):
        # Stream closed or error, return what we have
        # OSError: stream/file errors
        # EOFError: end of stream
        # ValueError: invalid stream state
        # CancelledError: task cancelled
        pass
    return b"".join(chunks)


async def x_read_stream_continuously__mutmut_10(
    stream: asyncio.StreamReader | None,
) -> bytes:
    """Continuously read from a stream until EOF.

    Args:
        stream: Stream to read from

    Returns:
        All bytes read from stream
    """
    if stream is None:
        return b""

    chunks: list[bytes] = []
    try:
        while True:
            chunk = await stream.read(8192)  # Read in 8KB chunks
            if chunk:
                break
            chunks.append(chunk)
    except (asyncio.CancelledError, OSError, EOFError, ValueError):
        # Stream closed or error, return what we have
        # OSError: stream/file errors
        # EOFError: end of stream
        # ValueError: invalid stream state
        # CancelledError: task cancelled
        pass
    return b"".join(chunks)


async def x_read_stream_continuously__mutmut_11(
    stream: asyncio.StreamReader | None,
) -> bytes:
    """Continuously read from a stream until EOF.

    Args:
        stream: Stream to read from

    Returns:
        All bytes read from stream
    """
    if stream is None:
        return b""

    chunks: list[bytes] = []
    try:
        while True:
            chunk = await stream.read(8192)  # Read in 8KB chunks
            if not chunk:
                return
            chunks.append(chunk)
    except (asyncio.CancelledError, OSError, EOFError, ValueError):
        # Stream closed or error, return what we have
        # OSError: stream/file errors
        # EOFError: end of stream
        # ValueError: invalid stream state
        # CancelledError: task cancelled
        pass
    return b"".join(chunks)


async def x_read_stream_continuously__mutmut_12(
    stream: asyncio.StreamReader | None,
) -> bytes:
    """Continuously read from a stream until EOF.

    Args:
        stream: Stream to read from

    Returns:
        All bytes read from stream
    """
    if stream is None:
        return b""

    chunks: list[bytes] = []
    try:
        while True:
            chunk = await stream.read(8192)  # Read in 8KB chunks
            if not chunk:
                break
            chunks.append(None)
    except (asyncio.CancelledError, OSError, EOFError, ValueError):
        # Stream closed or error, return what we have
        # OSError: stream/file errors
        # EOFError: end of stream
        # ValueError: invalid stream state
        # CancelledError: task cancelled
        pass
    return b"".join(chunks)


async def x_read_stream_continuously__mutmut_13(
    stream: asyncio.StreamReader | None,
) -> bytes:
    """Continuously read from a stream until EOF.

    Args:
        stream: Stream to read from

    Returns:
        All bytes read from stream
    """
    if stream is None:
        return b""

    chunks: list[bytes] = []
    try:
        while True:
            chunk = await stream.read(8192)  # Read in 8KB chunks
            if not chunk:
                break
            chunks.append(chunk)
    except (asyncio.CancelledError, OSError, EOFError, ValueError):
        # Stream closed or error, return what we have
        # OSError: stream/file errors
        # EOFError: end of stream
        # ValueError: invalid stream state
        # CancelledError: task cancelled
        pass
    return b"".join(None)


async def x_read_stream_continuously__mutmut_14(
    stream: asyncio.StreamReader | None,
) -> bytes:
    """Continuously read from a stream until EOF.

    Args:
        stream: Stream to read from

    Returns:
        All bytes read from stream
    """
    if stream is None:
        return b""

    chunks: list[bytes] = []
    try:
        while True:
            chunk = await stream.read(8192)  # Read in 8KB chunks
            if not chunk:
                break
            chunks.append(chunk)
    except (asyncio.CancelledError, OSError, EOFError, ValueError):
        # Stream closed or error, return what we have
        # OSError: stream/file errors
        # EOFError: end of stream
        # ValueError: invalid stream state
        # CancelledError: task cancelled
        pass
    return b"XXXX".join(chunks)


async def x_read_stream_continuously__mutmut_15(
    stream: asyncio.StreamReader | None,
) -> bytes:
    """Continuously read from a stream until EOF.

    Args:
        stream: Stream to read from

    Returns:
        All bytes read from stream
    """
    if stream is None:
        return b""

    chunks: list[bytes] = []
    try:
        while True:
            chunk = await stream.read(8192)  # Read in 8KB chunks
            if not chunk:
                break
            chunks.append(chunk)
    except (asyncio.CancelledError, OSError, EOFError, ValueError):
        # Stream closed or error, return what we have
        # OSError: stream/file errors
        # EOFError: end of stream
        # ValueError: invalid stream state
        # CancelledError: task cancelled
        pass
    return b"".join(chunks)


async def x_read_stream_continuously__mutmut_16(
    stream: asyncio.StreamReader | None,
) -> bytes:
    """Continuously read from a stream until EOF.

    Args:
        stream: Stream to read from

    Returns:
        All bytes read from stream
    """
    if stream is None:
        return b""

    chunks: list[bytes] = []
    try:
        while True:
            chunk = await stream.read(8192)  # Read in 8KB chunks
            if not chunk:
                break
            chunks.append(chunk)
    except (asyncio.CancelledError, OSError, EOFError, ValueError):
        # Stream closed or error, return what we have
        # OSError: stream/file errors
        # EOFError: end of stream
        # ValueError: invalid stream state
        # CancelledError: task cancelled
        pass
    return b"".join(chunks)


x_read_stream_continuously__mutmut_mutants: ClassVar[MutantDict] = {
    "x_read_stream_continuously__mutmut_1": x_read_stream_continuously__mutmut_1,
    "x_read_stream_continuously__mutmut_2": x_read_stream_continuously__mutmut_2,
    "x_read_stream_continuously__mutmut_3": x_read_stream_continuously__mutmut_3,
    "x_read_stream_continuously__mutmut_4": x_read_stream_continuously__mutmut_4,
    "x_read_stream_continuously__mutmut_5": x_read_stream_continuously__mutmut_5,
    "x_read_stream_continuously__mutmut_6": x_read_stream_continuously__mutmut_6,
    "x_read_stream_continuously__mutmut_7": x_read_stream_continuously__mutmut_7,
    "x_read_stream_continuously__mutmut_8": x_read_stream_continuously__mutmut_8,
    "x_read_stream_continuously__mutmut_9": x_read_stream_continuously__mutmut_9,
    "x_read_stream_continuously__mutmut_10": x_read_stream_continuously__mutmut_10,
    "x_read_stream_continuously__mutmut_11": x_read_stream_continuously__mutmut_11,
    "x_read_stream_continuously__mutmut_12": x_read_stream_continuously__mutmut_12,
    "x_read_stream_continuously__mutmut_13": x_read_stream_continuously__mutmut_13,
    "x_read_stream_continuously__mutmut_14": x_read_stream_continuously__mutmut_14,
    "x_read_stream_continuously__mutmut_15": x_read_stream_continuously__mutmut_15,
    "x_read_stream_continuously__mutmut_16": x_read_stream_continuously__mutmut_16,
}


def read_stream_continuously(*args, **kwargs):
    result = _mutmut_trampoline(
        x_read_stream_continuously__mutmut_orig, x_read_stream_continuously__mutmut_mutants, args, kwargs
    )
    return result


read_stream_continuously.__signature__ = _mutmut_signature(x_read_stream_continuously__mutmut_orig)
x_read_stream_continuously__mutmut_orig.__name__ = "x_read_stream_continuously"


async def x_communicate_with_timeout__mutmut_orig(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_1(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = None
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_2(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(None)
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_3(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(None))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_4(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = None

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_5(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(None)

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_6(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(None))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_7(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input or process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_8(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(None)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_9(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(None, timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_10(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=None)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_11(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_12(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(
                process.wait(),
            )
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_13(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = None
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_14(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = None
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_15(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    None,
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_16(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=None,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_17(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_18(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_19(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(None, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_20(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, None, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_21(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=None),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_22(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_23(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_24(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(
                        stdout_task,
                        stderr_task,
                    ),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_25(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=False),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_26(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=1.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_27(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(None):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_28(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(None, timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_29(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=None)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_30(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_31(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(
                    process.wait(),
                )

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_32(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=2.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_33(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = None
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_34(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b"XXXX"
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_35(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_36(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_37(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = None

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_38(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b"XXXX"

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_39(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_40(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_41(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                None,
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_42(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=None,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_43(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=None,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_44(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=None,
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_45(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=None,
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_46(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_47(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_48(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_49(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_50(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_51(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "XX⏱️ Async command timed outXX",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_52(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_53(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ ASYNC COMMAND TIMED OUT",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_54(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                None,
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_55(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code=None,
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_56(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=None,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_57(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=None,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_58(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_59(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_60(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_61(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_62(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_63(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_64(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_65(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_66(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="XXPROCESS_ASYNC_TIMEOUTXX",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_67(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="process_async_timeout",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=input)


async def x_communicate_with_timeout__mutmut_68(
    process: asyncio.subprocess.Process,
    input: bytes | None,
    timeout: float | None,
    cmd_str: str,
) -> tuple[bytes | None, bytes | None]:
    """Communicate with process with optional timeout.

    Uses background tasks to continuously read stdout/stderr to ensure
    no output is lost on timeout.

    Args:
        process: Subprocess to communicate with
        input: Input bytes for stdin
        timeout: Optional timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        Tuple of (stdout, stderr) bytes

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    if timeout:
        # Start background tasks to continuously read output streams
        stdout_task = asyncio.create_task(read_stream_continuously(process.stdout))
        stderr_task = asyncio.create_task(read_stream_continuously(process.stderr))

        # Write input if provided
        if input and process.stdin:
            process.stdin.write(input)
            await process.stdin.drain()
            process.stdin.close()
            await process.stdin.wait_closed()

        # Wait for process to complete with timeout
        try:
            await asyncio.wait_for(process.wait(), timeout=timeout)
            # Process completed successfully, get output from background tasks
            stdout = await stdout_task
            stderr = await stderr_task
            return (stdout if stdout else None, stderr if stderr else None)
        except builtins.TimeoutError as e:
            # Process timed out - kill it and capture whatever output we've accumulated
            process.kill()

            # Wait a bit for background tasks to finish reading any remaining data
            try:
                await asyncio.wait_for(
                    asyncio.gather(stdout_task, stderr_task, return_exceptions=True),
                    timeout=0.5,
                )
            except builtins.TimeoutError:
                # Even the cleanup timed out, cancel the tasks
                stdout_task.cancel()
                stderr_task.cancel()

            # Ensure process is cleaned up
            with contextlib.suppress(builtins.TimeoutError):
                # Process still won't die after 1s, not much more we can do
                await asyncio.wait_for(process.wait(), timeout=1.0)

            # Get whatever output was captured
            partial_stdout = stdout_task.result() if stdout_task.done() else b""
            partial_stderr = stderr_task.result() if stderr_task.done() else b""

            log.error(
                "⏱️ Async command timed out",
                command=cmd_str,
                timeout=timeout,
                captured_stdout_size=len(partial_stdout),
                captured_stderr_size=len(partial_stderr),
            )
            raise ProcessTimeoutError(
                f"Command timed out after {timeout}s: {cmd_str}",
                code="PROCESS_ASYNC_TIMEOUT",
                command=cmd_str,
                timeout_seconds=timeout,
                stdout=partial_stdout if partial_stdout else None,
                stderr=partial_stderr if partial_stderr else None,
            ) from e
    else:
        return await process.communicate(input=None)


x_communicate_with_timeout__mutmut_mutants: ClassVar[MutantDict] = {
    "x_communicate_with_timeout__mutmut_1": x_communicate_with_timeout__mutmut_1,
    "x_communicate_with_timeout__mutmut_2": x_communicate_with_timeout__mutmut_2,
    "x_communicate_with_timeout__mutmut_3": x_communicate_with_timeout__mutmut_3,
    "x_communicate_with_timeout__mutmut_4": x_communicate_with_timeout__mutmut_4,
    "x_communicate_with_timeout__mutmut_5": x_communicate_with_timeout__mutmut_5,
    "x_communicate_with_timeout__mutmut_6": x_communicate_with_timeout__mutmut_6,
    "x_communicate_with_timeout__mutmut_7": x_communicate_with_timeout__mutmut_7,
    "x_communicate_with_timeout__mutmut_8": x_communicate_with_timeout__mutmut_8,
    "x_communicate_with_timeout__mutmut_9": x_communicate_with_timeout__mutmut_9,
    "x_communicate_with_timeout__mutmut_10": x_communicate_with_timeout__mutmut_10,
    "x_communicate_with_timeout__mutmut_11": x_communicate_with_timeout__mutmut_11,
    "x_communicate_with_timeout__mutmut_12": x_communicate_with_timeout__mutmut_12,
    "x_communicate_with_timeout__mutmut_13": x_communicate_with_timeout__mutmut_13,
    "x_communicate_with_timeout__mutmut_14": x_communicate_with_timeout__mutmut_14,
    "x_communicate_with_timeout__mutmut_15": x_communicate_with_timeout__mutmut_15,
    "x_communicate_with_timeout__mutmut_16": x_communicate_with_timeout__mutmut_16,
    "x_communicate_with_timeout__mutmut_17": x_communicate_with_timeout__mutmut_17,
    "x_communicate_with_timeout__mutmut_18": x_communicate_with_timeout__mutmut_18,
    "x_communicate_with_timeout__mutmut_19": x_communicate_with_timeout__mutmut_19,
    "x_communicate_with_timeout__mutmut_20": x_communicate_with_timeout__mutmut_20,
    "x_communicate_with_timeout__mutmut_21": x_communicate_with_timeout__mutmut_21,
    "x_communicate_with_timeout__mutmut_22": x_communicate_with_timeout__mutmut_22,
    "x_communicate_with_timeout__mutmut_23": x_communicate_with_timeout__mutmut_23,
    "x_communicate_with_timeout__mutmut_24": x_communicate_with_timeout__mutmut_24,
    "x_communicate_with_timeout__mutmut_25": x_communicate_with_timeout__mutmut_25,
    "x_communicate_with_timeout__mutmut_26": x_communicate_with_timeout__mutmut_26,
    "x_communicate_with_timeout__mutmut_27": x_communicate_with_timeout__mutmut_27,
    "x_communicate_with_timeout__mutmut_28": x_communicate_with_timeout__mutmut_28,
    "x_communicate_with_timeout__mutmut_29": x_communicate_with_timeout__mutmut_29,
    "x_communicate_with_timeout__mutmut_30": x_communicate_with_timeout__mutmut_30,
    "x_communicate_with_timeout__mutmut_31": x_communicate_with_timeout__mutmut_31,
    "x_communicate_with_timeout__mutmut_32": x_communicate_with_timeout__mutmut_32,
    "x_communicate_with_timeout__mutmut_33": x_communicate_with_timeout__mutmut_33,
    "x_communicate_with_timeout__mutmut_34": x_communicate_with_timeout__mutmut_34,
    "x_communicate_with_timeout__mutmut_35": x_communicate_with_timeout__mutmut_35,
    "x_communicate_with_timeout__mutmut_36": x_communicate_with_timeout__mutmut_36,
    "x_communicate_with_timeout__mutmut_37": x_communicate_with_timeout__mutmut_37,
    "x_communicate_with_timeout__mutmut_38": x_communicate_with_timeout__mutmut_38,
    "x_communicate_with_timeout__mutmut_39": x_communicate_with_timeout__mutmut_39,
    "x_communicate_with_timeout__mutmut_40": x_communicate_with_timeout__mutmut_40,
    "x_communicate_with_timeout__mutmut_41": x_communicate_with_timeout__mutmut_41,
    "x_communicate_with_timeout__mutmut_42": x_communicate_with_timeout__mutmut_42,
    "x_communicate_with_timeout__mutmut_43": x_communicate_with_timeout__mutmut_43,
    "x_communicate_with_timeout__mutmut_44": x_communicate_with_timeout__mutmut_44,
    "x_communicate_with_timeout__mutmut_45": x_communicate_with_timeout__mutmut_45,
    "x_communicate_with_timeout__mutmut_46": x_communicate_with_timeout__mutmut_46,
    "x_communicate_with_timeout__mutmut_47": x_communicate_with_timeout__mutmut_47,
    "x_communicate_with_timeout__mutmut_48": x_communicate_with_timeout__mutmut_48,
    "x_communicate_with_timeout__mutmut_49": x_communicate_with_timeout__mutmut_49,
    "x_communicate_with_timeout__mutmut_50": x_communicate_with_timeout__mutmut_50,
    "x_communicate_with_timeout__mutmut_51": x_communicate_with_timeout__mutmut_51,
    "x_communicate_with_timeout__mutmut_52": x_communicate_with_timeout__mutmut_52,
    "x_communicate_with_timeout__mutmut_53": x_communicate_with_timeout__mutmut_53,
    "x_communicate_with_timeout__mutmut_54": x_communicate_with_timeout__mutmut_54,
    "x_communicate_with_timeout__mutmut_55": x_communicate_with_timeout__mutmut_55,
    "x_communicate_with_timeout__mutmut_56": x_communicate_with_timeout__mutmut_56,
    "x_communicate_with_timeout__mutmut_57": x_communicate_with_timeout__mutmut_57,
    "x_communicate_with_timeout__mutmut_58": x_communicate_with_timeout__mutmut_58,
    "x_communicate_with_timeout__mutmut_59": x_communicate_with_timeout__mutmut_59,
    "x_communicate_with_timeout__mutmut_60": x_communicate_with_timeout__mutmut_60,
    "x_communicate_with_timeout__mutmut_61": x_communicate_with_timeout__mutmut_61,
    "x_communicate_with_timeout__mutmut_62": x_communicate_with_timeout__mutmut_62,
    "x_communicate_with_timeout__mutmut_63": x_communicate_with_timeout__mutmut_63,
    "x_communicate_with_timeout__mutmut_64": x_communicate_with_timeout__mutmut_64,
    "x_communicate_with_timeout__mutmut_65": x_communicate_with_timeout__mutmut_65,
    "x_communicate_with_timeout__mutmut_66": x_communicate_with_timeout__mutmut_66,
    "x_communicate_with_timeout__mutmut_67": x_communicate_with_timeout__mutmut_67,
    "x_communicate_with_timeout__mutmut_68": x_communicate_with_timeout__mutmut_68,
}


def communicate_with_timeout(*args, **kwargs):
    result = _mutmut_trampoline(
        x_communicate_with_timeout__mutmut_orig, x_communicate_with_timeout__mutmut_mutants, args, kwargs
    )
    return result


communicate_with_timeout.__signature__ = _mutmut_signature(x_communicate_with_timeout__mutmut_orig)
x_communicate_with_timeout__mutmut_orig.__name__ = "x_communicate_with_timeout"


def x_create_completed_process_result__mutmut_orig(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors="replace") if stdout else ""
    stderr_str = stderr.decode(errors="replace") if stderr else ""

    return CompletedProcess(
        args=cmd if isinstance(cmd, list) else [cmd],
        returncode=process.returncode or 0,
        stdout=stdout_str,
        stderr=stderr_str,
        cwd=cwd,
        env=dict(env) if env else None,  # Only store caller overrides, not full run_env
    )


def x_create_completed_process_result__mutmut_1(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = None
    stderr_str = stderr.decode(errors="replace") if stderr else ""

    return CompletedProcess(
        args=cmd if isinstance(cmd, list) else [cmd],
        returncode=process.returncode or 0,
        stdout=stdout_str,
        stderr=stderr_str,
        cwd=cwd,
        env=dict(env) if env else None,  # Only store caller overrides, not full run_env
    )


def x_create_completed_process_result__mutmut_2(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors=None) if stdout else ""
    stderr_str = stderr.decode(errors="replace") if stderr else ""

    return CompletedProcess(
        args=cmd if isinstance(cmd, list) else [cmd],
        returncode=process.returncode or 0,
        stdout=stdout_str,
        stderr=stderr_str,
        cwd=cwd,
        env=dict(env) if env else None,  # Only store caller overrides, not full run_env
    )


def x_create_completed_process_result__mutmut_3(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors="XXreplaceXX") if stdout else ""
    stderr_str = stderr.decode(errors="replace") if stderr else ""

    return CompletedProcess(
        args=cmd if isinstance(cmd, list) else [cmd],
        returncode=process.returncode or 0,
        stdout=stdout_str,
        stderr=stderr_str,
        cwd=cwd,
        env=dict(env) if env else None,  # Only store caller overrides, not full run_env
    )


def x_create_completed_process_result__mutmut_4(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors="REPLACE") if stdout else ""
    stderr_str = stderr.decode(errors="replace") if stderr else ""

    return CompletedProcess(
        args=cmd if isinstance(cmd, list) else [cmd],
        returncode=process.returncode or 0,
        stdout=stdout_str,
        stderr=stderr_str,
        cwd=cwd,
        env=dict(env) if env else None,  # Only store caller overrides, not full run_env
    )


def x_create_completed_process_result__mutmut_5(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors="replace") if stdout else "XXXX"
    stderr_str = stderr.decode(errors="replace") if stderr else ""

    return CompletedProcess(
        args=cmd if isinstance(cmd, list) else [cmd],
        returncode=process.returncode or 0,
        stdout=stdout_str,
        stderr=stderr_str,
        cwd=cwd,
        env=dict(env) if env else None,  # Only store caller overrides, not full run_env
    )


def x_create_completed_process_result__mutmut_6(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors="replace") if stdout else ""
    stderr_str = None

    return CompletedProcess(
        args=cmd if isinstance(cmd, list) else [cmd],
        returncode=process.returncode or 0,
        stdout=stdout_str,
        stderr=stderr_str,
        cwd=cwd,
        env=dict(env) if env else None,  # Only store caller overrides, not full run_env
    )


def x_create_completed_process_result__mutmut_7(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors="replace") if stdout else ""
    stderr_str = stderr.decode(errors=None) if stderr else ""

    return CompletedProcess(
        args=cmd if isinstance(cmd, list) else [cmd],
        returncode=process.returncode or 0,
        stdout=stdout_str,
        stderr=stderr_str,
        cwd=cwd,
        env=dict(env) if env else None,  # Only store caller overrides, not full run_env
    )


def x_create_completed_process_result__mutmut_8(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors="replace") if stdout else ""
    stderr_str = stderr.decode(errors="XXreplaceXX") if stderr else ""

    return CompletedProcess(
        args=cmd if isinstance(cmd, list) else [cmd],
        returncode=process.returncode or 0,
        stdout=stdout_str,
        stderr=stderr_str,
        cwd=cwd,
        env=dict(env) if env else None,  # Only store caller overrides, not full run_env
    )


def x_create_completed_process_result__mutmut_9(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors="replace") if stdout else ""
    stderr_str = stderr.decode(errors="REPLACE") if stderr else ""

    return CompletedProcess(
        args=cmd if isinstance(cmd, list) else [cmd],
        returncode=process.returncode or 0,
        stdout=stdout_str,
        stderr=stderr_str,
        cwd=cwd,
        env=dict(env) if env else None,  # Only store caller overrides, not full run_env
    )


def x_create_completed_process_result__mutmut_10(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors="replace") if stdout else ""
    stderr_str = stderr.decode(errors="replace") if stderr else "XXXX"

    return CompletedProcess(
        args=cmd if isinstance(cmd, list) else [cmd],
        returncode=process.returncode or 0,
        stdout=stdout_str,
        stderr=stderr_str,
        cwd=cwd,
        env=dict(env) if env else None,  # Only store caller overrides, not full run_env
    )


def x_create_completed_process_result__mutmut_11(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors="replace") if stdout else ""
    stderr_str = stderr.decode(errors="replace") if stderr else ""

    return CompletedProcess(
        args=None,
        returncode=process.returncode or 0,
        stdout=stdout_str,
        stderr=stderr_str,
        cwd=cwd,
        env=dict(env) if env else None,  # Only store caller overrides, not full run_env
    )


def x_create_completed_process_result__mutmut_12(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors="replace") if stdout else ""
    stderr_str = stderr.decode(errors="replace") if stderr else ""

    return CompletedProcess(
        args=cmd if isinstance(cmd, list) else [cmd],
        returncode=None,
        stdout=stdout_str,
        stderr=stderr_str,
        cwd=cwd,
        env=dict(env) if env else None,  # Only store caller overrides, not full run_env
    )


def x_create_completed_process_result__mutmut_13(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors="replace") if stdout else ""
    stderr_str = stderr.decode(errors="replace") if stderr else ""

    return CompletedProcess(
        args=cmd if isinstance(cmd, list) else [cmd],
        returncode=process.returncode or 0,
        stdout=None,
        stderr=stderr_str,
        cwd=cwd,
        env=dict(env) if env else None,  # Only store caller overrides, not full run_env
    )


def x_create_completed_process_result__mutmut_14(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors="replace") if stdout else ""
    stderr_str = stderr.decode(errors="replace") if stderr else ""

    return CompletedProcess(
        args=cmd if isinstance(cmd, list) else [cmd],
        returncode=process.returncode or 0,
        stdout=stdout_str,
        stderr=None,
        cwd=cwd,
        env=dict(env) if env else None,  # Only store caller overrides, not full run_env
    )


def x_create_completed_process_result__mutmut_15(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors="replace") if stdout else ""
    stderr_str = stderr.decode(errors="replace") if stderr else ""

    return CompletedProcess(
        args=cmd if isinstance(cmd, list) else [cmd],
        returncode=process.returncode or 0,
        stdout=stdout_str,
        stderr=stderr_str,
        cwd=None,
        env=dict(env) if env else None,  # Only store caller overrides, not full run_env
    )


def x_create_completed_process_result__mutmut_16(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors="replace") if stdout else ""
    stderr_str = stderr.decode(errors="replace") if stderr else ""

    return CompletedProcess(
        args=cmd if isinstance(cmd, list) else [cmd],
        returncode=process.returncode or 0,
        stdout=stdout_str,
        stderr=stderr_str,
        cwd=cwd,
        env=None,  # Only store caller overrides, not full run_env
    )


def x_create_completed_process_result__mutmut_17(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors="replace") if stdout else ""
    stderr_str = stderr.decode(errors="replace") if stderr else ""

    return CompletedProcess(
        returncode=process.returncode or 0,
        stdout=stdout_str,
        stderr=stderr_str,
        cwd=cwd,
        env=dict(env) if env else None,  # Only store caller overrides, not full run_env
    )


def x_create_completed_process_result__mutmut_18(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors="replace") if stdout else ""
    stderr_str = stderr.decode(errors="replace") if stderr else ""

    return CompletedProcess(
        args=cmd if isinstance(cmd, list) else [cmd],
        stdout=stdout_str,
        stderr=stderr_str,
        cwd=cwd,
        env=dict(env) if env else None,  # Only store caller overrides, not full run_env
    )


def x_create_completed_process_result__mutmut_19(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors="replace") if stdout else ""
    stderr_str = stderr.decode(errors="replace") if stderr else ""

    return CompletedProcess(
        args=cmd if isinstance(cmd, list) else [cmd],
        returncode=process.returncode or 0,
        stderr=stderr_str,
        cwd=cwd,
        env=dict(env) if env else None,  # Only store caller overrides, not full run_env
    )


def x_create_completed_process_result__mutmut_20(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors="replace") if stdout else ""
    stderr_str = stderr.decode(errors="replace") if stderr else ""

    return CompletedProcess(
        args=cmd if isinstance(cmd, list) else [cmd],
        returncode=process.returncode or 0,
        stdout=stdout_str,
        cwd=cwd,
        env=dict(env) if env else None,  # Only store caller overrides, not full run_env
    )


def x_create_completed_process_result__mutmut_21(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors="replace") if stdout else ""
    stderr_str = stderr.decode(errors="replace") if stderr else ""

    return CompletedProcess(
        args=cmd if isinstance(cmd, list) else [cmd],
        returncode=process.returncode or 0,
        stdout=stdout_str,
        stderr=stderr_str,
        env=dict(env) if env else None,  # Only store caller overrides, not full run_env
    )


def x_create_completed_process_result__mutmut_22(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors="replace") if stdout else ""
    stderr_str = stderr.decode(errors="replace") if stderr else ""

    return CompletedProcess(
        args=cmd if isinstance(cmd, list) else [cmd],
        returncode=process.returncode or 0,
        stdout=stdout_str,
        stderr=stderr_str,
        cwd=cwd,
    )


def x_create_completed_process_result__mutmut_23(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors="replace") if stdout else ""
    stderr_str = stderr.decode(errors="replace") if stderr else ""

    return CompletedProcess(
        args=cmd if isinstance(cmd, list) else [cmd],
        returncode=process.returncode and 0,
        stdout=stdout_str,
        stderr=stderr_str,
        cwd=cwd,
        env=dict(env) if env else None,  # Only store caller overrides, not full run_env
    )


def x_create_completed_process_result__mutmut_24(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors="replace") if stdout else ""
    stderr_str = stderr.decode(errors="replace") if stderr else ""

    return CompletedProcess(
        args=cmd if isinstance(cmd, list) else [cmd],
        returncode=process.returncode or 1,
        stdout=stdout_str,
        stderr=stderr_str,
        cwd=cwd,
        env=dict(env) if env else None,  # Only store caller overrides, not full run_env
    )


def x_create_completed_process_result__mutmut_25(
    cmd: list[str] | str,
    process: asyncio.subprocess.Process,
    stdout: bytes | None,
    stderr: bytes | None,
    cwd: str | None,
    env: Mapping[str, str] | None,
    run_env: dict[str, str],
) -> CompletedProcess:
    """Create a CompletedProcess from subprocess results.

    Args:
        cmd: Command that was executed
        process: Completed subprocess
        stdout: Standard output bytes
        stderr: Standard error bytes
        cwd: Working directory
        env: Original environment mapping
        run_env: Actual environment used

    Returns:
        CompletedProcess with results
    """
    stdout_str = stdout.decode(errors="replace") if stdout else ""
    stderr_str = stderr.decode(errors="replace") if stderr else ""

    return CompletedProcess(
        args=cmd if isinstance(cmd, list) else [cmd],
        returncode=process.returncode or 0,
        stdout=stdout_str,
        stderr=stderr_str,
        cwd=cwd,
        env=dict(None) if env else None,  # Only store caller overrides, not full run_env
    )


x_create_completed_process_result__mutmut_mutants: ClassVar[MutantDict] = {
    "x_create_completed_process_result__mutmut_1": x_create_completed_process_result__mutmut_1,
    "x_create_completed_process_result__mutmut_2": x_create_completed_process_result__mutmut_2,
    "x_create_completed_process_result__mutmut_3": x_create_completed_process_result__mutmut_3,
    "x_create_completed_process_result__mutmut_4": x_create_completed_process_result__mutmut_4,
    "x_create_completed_process_result__mutmut_5": x_create_completed_process_result__mutmut_5,
    "x_create_completed_process_result__mutmut_6": x_create_completed_process_result__mutmut_6,
    "x_create_completed_process_result__mutmut_7": x_create_completed_process_result__mutmut_7,
    "x_create_completed_process_result__mutmut_8": x_create_completed_process_result__mutmut_8,
    "x_create_completed_process_result__mutmut_9": x_create_completed_process_result__mutmut_9,
    "x_create_completed_process_result__mutmut_10": x_create_completed_process_result__mutmut_10,
    "x_create_completed_process_result__mutmut_11": x_create_completed_process_result__mutmut_11,
    "x_create_completed_process_result__mutmut_12": x_create_completed_process_result__mutmut_12,
    "x_create_completed_process_result__mutmut_13": x_create_completed_process_result__mutmut_13,
    "x_create_completed_process_result__mutmut_14": x_create_completed_process_result__mutmut_14,
    "x_create_completed_process_result__mutmut_15": x_create_completed_process_result__mutmut_15,
    "x_create_completed_process_result__mutmut_16": x_create_completed_process_result__mutmut_16,
    "x_create_completed_process_result__mutmut_17": x_create_completed_process_result__mutmut_17,
    "x_create_completed_process_result__mutmut_18": x_create_completed_process_result__mutmut_18,
    "x_create_completed_process_result__mutmut_19": x_create_completed_process_result__mutmut_19,
    "x_create_completed_process_result__mutmut_20": x_create_completed_process_result__mutmut_20,
    "x_create_completed_process_result__mutmut_21": x_create_completed_process_result__mutmut_21,
    "x_create_completed_process_result__mutmut_22": x_create_completed_process_result__mutmut_22,
    "x_create_completed_process_result__mutmut_23": x_create_completed_process_result__mutmut_23,
    "x_create_completed_process_result__mutmut_24": x_create_completed_process_result__mutmut_24,
    "x_create_completed_process_result__mutmut_25": x_create_completed_process_result__mutmut_25,
}


def create_completed_process_result(*args, **kwargs):
    result = _mutmut_trampoline(
        x_create_completed_process_result__mutmut_orig,
        x_create_completed_process_result__mutmut_mutants,
        args,
        kwargs,
    )
    return result


create_completed_process_result.__signature__ = _mutmut_signature(
    x_create_completed_process_result__mutmut_orig
)
x_create_completed_process_result__mutmut_orig.__name__ = "x_create_completed_process_result"


def x_check_process_success__mutmut_orig(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            "❌ Async command failed",
            command=cmd_str,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_FAILED",
            command=cmd_str,
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_1(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check or process.returncode != 0:
        log.error(
            "❌ Async command failed",
            command=cmd_str,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_FAILED",
            command=cmd_str,
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_2(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode == 0:
        log.error(
            "❌ Async command failed",
            command=cmd_str,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_FAILED",
            command=cmd_str,
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_3(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 1:
        log.error(
            "❌ Async command failed",
            command=cmd_str,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_FAILED",
            command=cmd_str,
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_4(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            None,
            command=cmd_str,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_FAILED",
            command=cmd_str,
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_5(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            "❌ Async command failed",
            command=None,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_FAILED",
            command=cmd_str,
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_6(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            "❌ Async command failed",
            command=cmd_str,
            returncode=None,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_FAILED",
            command=cmd_str,
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_7(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            "❌ Async command failed",
            command=cmd_str,
            returncode=process.returncode,
            stderr=None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_FAILED",
            command=cmd_str,
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_8(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            command=cmd_str,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_FAILED",
            command=cmd_str,
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_9(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            "❌ Async command failed",
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_FAILED",
            command=cmd_str,
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_10(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            "❌ Async command failed",
            command=cmd_str,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_FAILED",
            command=cmd_str,
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_11(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            "❌ Async command failed",
            command=cmd_str,
            returncode=process.returncode,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_FAILED",
            command=cmd_str,
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_12(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            "XX❌ Async command failedXX",
            command=cmd_str,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_FAILED",
            command=cmd_str,
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_13(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            "❌ async command failed",
            command=cmd_str,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_FAILED",
            command=cmd_str,
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_14(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            "❌ ASYNC COMMAND FAILED",
            command=cmd_str,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_FAILED",
            command=cmd_str,
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_15(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            "❌ Async command failed",
            command=cmd_str,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            None,
            code="PROCESS_ASYNC_FAILED",
            command=cmd_str,
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_16(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            "❌ Async command failed",
            command=cmd_str,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code=None,
            command=cmd_str,
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_17(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            "❌ Async command failed",
            command=cmd_str,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_FAILED",
            command=None,
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_18(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            "❌ Async command failed",
            command=cmd_str,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_FAILED",
            command=cmd_str,
            return_code=None,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_19(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            "❌ Async command failed",
            command=cmd_str,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_FAILED",
            command=cmd_str,
            return_code=process.returncode,
            stdout=None,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_20(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            "❌ Async command failed",
            command=cmd_str,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_FAILED",
            command=cmd_str,
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=None,
        )


def x_check_process_success__mutmut_21(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            "❌ Async command failed",
            command=cmd_str,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            code="PROCESS_ASYNC_FAILED",
            command=cmd_str,
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_22(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            "❌ Async command failed",
            command=cmd_str,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            command=cmd_str,
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_23(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            "❌ Async command failed",
            command=cmd_str,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_FAILED",
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_24(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            "❌ Async command failed",
            command=cmd_str,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_FAILED",
            command=cmd_str,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_25(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            "❌ Async command failed",
            command=cmd_str,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_FAILED",
            command=cmd_str,
            return_code=process.returncode,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_26(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            "❌ Async command failed",
            command=cmd_str,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_FAILED",
            command=cmd_str,
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
        )


def x_check_process_success__mutmut_27(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            "❌ Async command failed",
            command=cmd_str,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="XXPROCESS_ASYNC_FAILEDXX",
            command=cmd_str,
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


def x_check_process_success__mutmut_28(
    process: asyncio.subprocess.Process,
    cmd_str: str,
    capture_output: bool,
    stdout_str: str,
    stderr_str: str,
    check: bool,
) -> None:
    """Check if process succeeded and raise if needed.

    Args:
        process: Completed subprocess
        cmd_str: Command string for error messages
        capture_output: Whether output was captured
        stdout_str: Standard output
        stderr_str: Standard error
        check: Whether to raise on non-zero exit

    Raises:
        ProcessError: If check=True and process failed
    """
    if check and process.returncode != 0:
        log.error(
            "❌ Async command failed",
            command=cmd_str,
            returncode=process.returncode,
            stderr=stderr_str if capture_output else None,
        )
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="process_async_failed",
            command=cmd_str,
            return_code=process.returncode,
            stdout=stdout_str if capture_output else None,
            stderr=stderr_str if capture_output else None,
        )


x_check_process_success__mutmut_mutants: ClassVar[MutantDict] = {
    "x_check_process_success__mutmut_1": x_check_process_success__mutmut_1,
    "x_check_process_success__mutmut_2": x_check_process_success__mutmut_2,
    "x_check_process_success__mutmut_3": x_check_process_success__mutmut_3,
    "x_check_process_success__mutmut_4": x_check_process_success__mutmut_4,
    "x_check_process_success__mutmut_5": x_check_process_success__mutmut_5,
    "x_check_process_success__mutmut_6": x_check_process_success__mutmut_6,
    "x_check_process_success__mutmut_7": x_check_process_success__mutmut_7,
    "x_check_process_success__mutmut_8": x_check_process_success__mutmut_8,
    "x_check_process_success__mutmut_9": x_check_process_success__mutmut_9,
    "x_check_process_success__mutmut_10": x_check_process_success__mutmut_10,
    "x_check_process_success__mutmut_11": x_check_process_success__mutmut_11,
    "x_check_process_success__mutmut_12": x_check_process_success__mutmut_12,
    "x_check_process_success__mutmut_13": x_check_process_success__mutmut_13,
    "x_check_process_success__mutmut_14": x_check_process_success__mutmut_14,
    "x_check_process_success__mutmut_15": x_check_process_success__mutmut_15,
    "x_check_process_success__mutmut_16": x_check_process_success__mutmut_16,
    "x_check_process_success__mutmut_17": x_check_process_success__mutmut_17,
    "x_check_process_success__mutmut_18": x_check_process_success__mutmut_18,
    "x_check_process_success__mutmut_19": x_check_process_success__mutmut_19,
    "x_check_process_success__mutmut_20": x_check_process_success__mutmut_20,
    "x_check_process_success__mutmut_21": x_check_process_success__mutmut_21,
    "x_check_process_success__mutmut_22": x_check_process_success__mutmut_22,
    "x_check_process_success__mutmut_23": x_check_process_success__mutmut_23,
    "x_check_process_success__mutmut_24": x_check_process_success__mutmut_24,
    "x_check_process_success__mutmut_25": x_check_process_success__mutmut_25,
    "x_check_process_success__mutmut_26": x_check_process_success__mutmut_26,
    "x_check_process_success__mutmut_27": x_check_process_success__mutmut_27,
    "x_check_process_success__mutmut_28": x_check_process_success__mutmut_28,
}


def check_process_success(*args, **kwargs):
    result = _mutmut_trampoline(
        x_check_process_success__mutmut_orig, x_check_process_success__mutmut_mutants, args, kwargs
    )
    return result


check_process_success.__signature__ = _mutmut_signature(x_check_process_success__mutmut_orig)
x_check_process_success__mutmut_orig.__name__ = "x_check_process_success"


async def x_cleanup_process__mutmut_orig(process: asyncio.subprocess.Process | None) -> None:
    """Clean up process resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.PIPE and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_process__mutmut_1(process: asyncio.subprocess.Process | None) -> None:
    """Clean up process resources.

    Args:
        process: Subprocess to clean up
    """
    if process:
        return

    # Close pipes if they exist
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.PIPE and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_process__mutmut_2(process: asyncio.subprocess.Process | None) -> None:
    """Clean up process resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist
    if process.stdin or not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.PIPE and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_process__mutmut_3(process: asyncio.subprocess.Process | None) -> None:
    """Clean up process resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist
    if process.stdin and process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.PIPE and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_process__mutmut_4(process: asyncio.subprocess.Process | None) -> None:
    """Clean up process resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout or not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.PIPE and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_process__mutmut_5(process: asyncio.subprocess.Process | None) -> None:
    """Clean up process resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.PIPE and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_process__mutmut_6(process: asyncio.subprocess.Process | None) -> None:
    """Clean up process resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.PIPE or not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_process__mutmut_7(process: asyncio.subprocess.Process | None) -> None:
    """Clean up process resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr or process.stderr != asyncio.subprocess.PIPE and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_process__mutmut_8(process: asyncio.subprocess.Process | None) -> None:
    """Clean up process resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr == asyncio.subprocess.PIPE and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_process__mutmut_9(process: asyncio.subprocess.Process | None) -> None:
    """Clean up process resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.PIPE and process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_process__mutmut_10(process: asyncio.subprocess.Process | None) -> None:
    """Clean up process resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.PIPE and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is not None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_process__mutmut_11(process: asyncio.subprocess.Process | None) -> None:
    """Clean up process resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.PIPE and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(None, timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_process__mutmut_12(process: asyncio.subprocess.Process | None) -> None:
    """Clean up process resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.PIPE and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=None)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_process__mutmut_13(process: asyncio.subprocess.Process | None) -> None:
    """Clean up process resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.PIPE and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_process__mutmut_14(process: asyncio.subprocess.Process | None) -> None:
    """Clean up process resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.PIPE and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(
                process.wait(),
            )
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_process__mutmut_15(process: asyncio.subprocess.Process | None) -> None:
    """Clean up process resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.PIPE and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=2.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


x_cleanup_process__mutmut_mutants: ClassVar[MutantDict] = {
    "x_cleanup_process__mutmut_1": x_cleanup_process__mutmut_1,
    "x_cleanup_process__mutmut_2": x_cleanup_process__mutmut_2,
    "x_cleanup_process__mutmut_3": x_cleanup_process__mutmut_3,
    "x_cleanup_process__mutmut_4": x_cleanup_process__mutmut_4,
    "x_cleanup_process__mutmut_5": x_cleanup_process__mutmut_5,
    "x_cleanup_process__mutmut_6": x_cleanup_process__mutmut_6,
    "x_cleanup_process__mutmut_7": x_cleanup_process__mutmut_7,
    "x_cleanup_process__mutmut_8": x_cleanup_process__mutmut_8,
    "x_cleanup_process__mutmut_9": x_cleanup_process__mutmut_9,
    "x_cleanup_process__mutmut_10": x_cleanup_process__mutmut_10,
    "x_cleanup_process__mutmut_11": x_cleanup_process__mutmut_11,
    "x_cleanup_process__mutmut_12": x_cleanup_process__mutmut_12,
    "x_cleanup_process__mutmut_13": x_cleanup_process__mutmut_13,
    "x_cleanup_process__mutmut_14": x_cleanup_process__mutmut_14,
    "x_cleanup_process__mutmut_15": x_cleanup_process__mutmut_15,
}


def cleanup_process(*args, **kwargs):
    result = _mutmut_trampoline(
        x_cleanup_process__mutmut_orig, x_cleanup_process__mutmut_mutants, args, kwargs
    )
    return result


cleanup_process.__signature__ = _mutmut_signature(x_cleanup_process__mutmut_orig)
x_cleanup_process__mutmut_orig.__name__ = "x_cleanup_process"


async def x_async_run__mutmut_orig(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_1(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = False,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_2(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = False,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_3(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = True,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_4(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = None
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_5(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(None) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_6(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = "XX XX".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_7(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(None)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_8(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = None
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_9(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(None)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_10(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace(None, command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_11(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=None, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_12(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_13(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace(command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_14(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_15(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace(
        "🚀 Running async command",
        command=masked_cmd,
    )

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_16(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("XX🚀 Running async commandXX", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_17(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_18(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 RUNNING ASYNC COMMAND", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_19(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(None) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_20(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) or not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_21(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_22(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            None,
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_23(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code=None,
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_24(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected=None,
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_25(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual=None,
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_26(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_27(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_28(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_29(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_30(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "XXString commands require explicit shell=True for security. XX"
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_31(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "string commands require explicit shell=true for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_32(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "STRING COMMANDS REQUIRE EXPLICIT SHELL=TRUE FOR SECURITY. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_33(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "XXUse async_shell() for shell commands or pass a list for direct execution.XX",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_34(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_35(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "USE ASYNC_SHELL() FOR SHELL COMMANDS OR PASS A LIST FOR DIRECT EXECUTION.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_36(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="XXINVALID_COMMAND_TYPEXX",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_37(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="invalid_command_type",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_38(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="XXlist[str] or (str with shell=True)XX",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_39(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=true)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_40(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="LIST[STR] OR (STR WITH SHELL=TRUE)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_41(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="XXstr without shell=TrueXX",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_42(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=true",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_43(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="STR WITHOUT SHELL=TRUE",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_44(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = None
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_45(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(None)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_46(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = None

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_47(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(None) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_48(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = ""
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_49(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = None

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_50(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(
            None, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs
        )

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_51(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, None, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_52(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, None, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_53(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, None, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_54(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, None, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_55(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, None, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_56(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, None, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_57(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, None)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_58(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_59(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_60(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_61(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_62(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_63(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_64(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_65(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(
            cmd,
            cmd_str,
            shell,
            cwd_str,
            run_env,
            capture_output,
            input,
        )

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_66(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = None

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_67(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(None, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_68(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, None, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_69(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, None, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_70(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, None)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_71(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_72(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_73(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_74(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(
                process,
                input,
                timeout,
            )

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_75(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = None

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_76(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(None, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_77(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, None, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_78(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, None, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_79(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, None, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_80(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, None, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_81(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, None, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_82(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, None)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_83(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_84(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_85(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_86(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_87(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_88(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_89(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(
                cmd,
                process,
                stdout,
                stderr,
                cwd_str,
                env,
            )

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_90(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(None, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_91(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, None, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_92(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, None, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_93(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, None, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_94(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, None, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_95(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, None)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_96(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_97(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_98(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_99(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_100(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_101(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(
                process,
                cmd_str,
                capture_output,
                completed.stdout,
                completed.stderr,
            )

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_102(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                None,
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_103(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=None,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_104(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=None,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_105(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_106(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_107(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_108(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "XX✅ Async command completedXX",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_109(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_110(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ ASYNC COMMAND COMPLETED",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_111(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(None)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_112(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            None,
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_113(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=None,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_114(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=None,
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_115(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_116(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_117(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_118(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "XX💥 Async command execution failedXX",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_119(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_120(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 ASYNC COMMAND EXECUTION FAILED",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_121(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(None),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_122(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            None,
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_123(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code=None,
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_124(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=None,
        ) from e


async def x_async_run__mutmut_125(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_126(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_127(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
        ) from e


async def x_async_run__mutmut_128(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="XXPROCESS_ASYNC_EXECUTION_FAILEDXX",
            command=cmd_str,
        ) from e


async def x_async_run__mutmut_129(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    input: bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        shell: Whether to execute via shell
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If command type and shell parameter mismatch
        ProcessError: If command fails and check=True
        ProcessTimeoutError: If timeout is exceeded
    """
    # Mask secrets in command for logging
    from provide.foundation.security import mask_command

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    masked_cmd = mask_command(cmd_str)
    log.trace("🚀 Running async command", command=masked_cmd, cwd=str(cwd) if cwd else None)

    # Validate command type and shell parameter
    if isinstance(cmd, str) and not shell:
        raise ValidationError(
            "String commands require explicit shell=True for security. "
            "Use async_shell() for shell commands or pass a list for direct execution.",
            code="INVALID_COMMAND_TYPE",
            expected="list[str] or (str with shell=True)",
            actual="str without shell=True",
        )

    # Prepare environment and convert Path to string
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_subprocess(cmd, cmd_str, shell, cwd_str, run_env, capture_output, input, kwargs)

        try:
            # Communicate with process
            stdout, stderr = await communicate_with_timeout(process, input, timeout, cmd_str)

            # Create completed process
            completed = create_completed_process_result(cmd, process, stdout, stderr, cwd_str, env, run_env)

            # Check for success
            check_process_success(process, cmd_str, capture_output, completed.stdout, completed.stderr, check)

            log.debug(
                "✅ Async command completed",
                command=cmd_str,
                returncode=process.returncode,
            )

            return completed
        finally:
            await cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError | ValidationError):
            raise

        log.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="process_async_execution_failed",
            command=cmd_str,
        ) from e


x_async_run__mutmut_mutants: ClassVar[MutantDict] = {
    "x_async_run__mutmut_1": x_async_run__mutmut_1,
    "x_async_run__mutmut_2": x_async_run__mutmut_2,
    "x_async_run__mutmut_3": x_async_run__mutmut_3,
    "x_async_run__mutmut_4": x_async_run__mutmut_4,
    "x_async_run__mutmut_5": x_async_run__mutmut_5,
    "x_async_run__mutmut_6": x_async_run__mutmut_6,
    "x_async_run__mutmut_7": x_async_run__mutmut_7,
    "x_async_run__mutmut_8": x_async_run__mutmut_8,
    "x_async_run__mutmut_9": x_async_run__mutmut_9,
    "x_async_run__mutmut_10": x_async_run__mutmut_10,
    "x_async_run__mutmut_11": x_async_run__mutmut_11,
    "x_async_run__mutmut_12": x_async_run__mutmut_12,
    "x_async_run__mutmut_13": x_async_run__mutmut_13,
    "x_async_run__mutmut_14": x_async_run__mutmut_14,
    "x_async_run__mutmut_15": x_async_run__mutmut_15,
    "x_async_run__mutmut_16": x_async_run__mutmut_16,
    "x_async_run__mutmut_17": x_async_run__mutmut_17,
    "x_async_run__mutmut_18": x_async_run__mutmut_18,
    "x_async_run__mutmut_19": x_async_run__mutmut_19,
    "x_async_run__mutmut_20": x_async_run__mutmut_20,
    "x_async_run__mutmut_21": x_async_run__mutmut_21,
    "x_async_run__mutmut_22": x_async_run__mutmut_22,
    "x_async_run__mutmut_23": x_async_run__mutmut_23,
    "x_async_run__mutmut_24": x_async_run__mutmut_24,
    "x_async_run__mutmut_25": x_async_run__mutmut_25,
    "x_async_run__mutmut_26": x_async_run__mutmut_26,
    "x_async_run__mutmut_27": x_async_run__mutmut_27,
    "x_async_run__mutmut_28": x_async_run__mutmut_28,
    "x_async_run__mutmut_29": x_async_run__mutmut_29,
    "x_async_run__mutmut_30": x_async_run__mutmut_30,
    "x_async_run__mutmut_31": x_async_run__mutmut_31,
    "x_async_run__mutmut_32": x_async_run__mutmut_32,
    "x_async_run__mutmut_33": x_async_run__mutmut_33,
    "x_async_run__mutmut_34": x_async_run__mutmut_34,
    "x_async_run__mutmut_35": x_async_run__mutmut_35,
    "x_async_run__mutmut_36": x_async_run__mutmut_36,
    "x_async_run__mutmut_37": x_async_run__mutmut_37,
    "x_async_run__mutmut_38": x_async_run__mutmut_38,
    "x_async_run__mutmut_39": x_async_run__mutmut_39,
    "x_async_run__mutmut_40": x_async_run__mutmut_40,
    "x_async_run__mutmut_41": x_async_run__mutmut_41,
    "x_async_run__mutmut_42": x_async_run__mutmut_42,
    "x_async_run__mutmut_43": x_async_run__mutmut_43,
    "x_async_run__mutmut_44": x_async_run__mutmut_44,
    "x_async_run__mutmut_45": x_async_run__mutmut_45,
    "x_async_run__mutmut_46": x_async_run__mutmut_46,
    "x_async_run__mutmut_47": x_async_run__mutmut_47,
    "x_async_run__mutmut_48": x_async_run__mutmut_48,
    "x_async_run__mutmut_49": x_async_run__mutmut_49,
    "x_async_run__mutmut_50": x_async_run__mutmut_50,
    "x_async_run__mutmut_51": x_async_run__mutmut_51,
    "x_async_run__mutmut_52": x_async_run__mutmut_52,
    "x_async_run__mutmut_53": x_async_run__mutmut_53,
    "x_async_run__mutmut_54": x_async_run__mutmut_54,
    "x_async_run__mutmut_55": x_async_run__mutmut_55,
    "x_async_run__mutmut_56": x_async_run__mutmut_56,
    "x_async_run__mutmut_57": x_async_run__mutmut_57,
    "x_async_run__mutmut_58": x_async_run__mutmut_58,
    "x_async_run__mutmut_59": x_async_run__mutmut_59,
    "x_async_run__mutmut_60": x_async_run__mutmut_60,
    "x_async_run__mutmut_61": x_async_run__mutmut_61,
    "x_async_run__mutmut_62": x_async_run__mutmut_62,
    "x_async_run__mutmut_63": x_async_run__mutmut_63,
    "x_async_run__mutmut_64": x_async_run__mutmut_64,
    "x_async_run__mutmut_65": x_async_run__mutmut_65,
    "x_async_run__mutmut_66": x_async_run__mutmut_66,
    "x_async_run__mutmut_67": x_async_run__mutmut_67,
    "x_async_run__mutmut_68": x_async_run__mutmut_68,
    "x_async_run__mutmut_69": x_async_run__mutmut_69,
    "x_async_run__mutmut_70": x_async_run__mutmut_70,
    "x_async_run__mutmut_71": x_async_run__mutmut_71,
    "x_async_run__mutmut_72": x_async_run__mutmut_72,
    "x_async_run__mutmut_73": x_async_run__mutmut_73,
    "x_async_run__mutmut_74": x_async_run__mutmut_74,
    "x_async_run__mutmut_75": x_async_run__mutmut_75,
    "x_async_run__mutmut_76": x_async_run__mutmut_76,
    "x_async_run__mutmut_77": x_async_run__mutmut_77,
    "x_async_run__mutmut_78": x_async_run__mutmut_78,
    "x_async_run__mutmut_79": x_async_run__mutmut_79,
    "x_async_run__mutmut_80": x_async_run__mutmut_80,
    "x_async_run__mutmut_81": x_async_run__mutmut_81,
    "x_async_run__mutmut_82": x_async_run__mutmut_82,
    "x_async_run__mutmut_83": x_async_run__mutmut_83,
    "x_async_run__mutmut_84": x_async_run__mutmut_84,
    "x_async_run__mutmut_85": x_async_run__mutmut_85,
    "x_async_run__mutmut_86": x_async_run__mutmut_86,
    "x_async_run__mutmut_87": x_async_run__mutmut_87,
    "x_async_run__mutmut_88": x_async_run__mutmut_88,
    "x_async_run__mutmut_89": x_async_run__mutmut_89,
    "x_async_run__mutmut_90": x_async_run__mutmut_90,
    "x_async_run__mutmut_91": x_async_run__mutmut_91,
    "x_async_run__mutmut_92": x_async_run__mutmut_92,
    "x_async_run__mutmut_93": x_async_run__mutmut_93,
    "x_async_run__mutmut_94": x_async_run__mutmut_94,
    "x_async_run__mutmut_95": x_async_run__mutmut_95,
    "x_async_run__mutmut_96": x_async_run__mutmut_96,
    "x_async_run__mutmut_97": x_async_run__mutmut_97,
    "x_async_run__mutmut_98": x_async_run__mutmut_98,
    "x_async_run__mutmut_99": x_async_run__mutmut_99,
    "x_async_run__mutmut_100": x_async_run__mutmut_100,
    "x_async_run__mutmut_101": x_async_run__mutmut_101,
    "x_async_run__mutmut_102": x_async_run__mutmut_102,
    "x_async_run__mutmut_103": x_async_run__mutmut_103,
    "x_async_run__mutmut_104": x_async_run__mutmut_104,
    "x_async_run__mutmut_105": x_async_run__mutmut_105,
    "x_async_run__mutmut_106": x_async_run__mutmut_106,
    "x_async_run__mutmut_107": x_async_run__mutmut_107,
    "x_async_run__mutmut_108": x_async_run__mutmut_108,
    "x_async_run__mutmut_109": x_async_run__mutmut_109,
    "x_async_run__mutmut_110": x_async_run__mutmut_110,
    "x_async_run__mutmut_111": x_async_run__mutmut_111,
    "x_async_run__mutmut_112": x_async_run__mutmut_112,
    "x_async_run__mutmut_113": x_async_run__mutmut_113,
    "x_async_run__mutmut_114": x_async_run__mutmut_114,
    "x_async_run__mutmut_115": x_async_run__mutmut_115,
    "x_async_run__mutmut_116": x_async_run__mutmut_116,
    "x_async_run__mutmut_117": x_async_run__mutmut_117,
    "x_async_run__mutmut_118": x_async_run__mutmut_118,
    "x_async_run__mutmut_119": x_async_run__mutmut_119,
    "x_async_run__mutmut_120": x_async_run__mutmut_120,
    "x_async_run__mutmut_121": x_async_run__mutmut_121,
    "x_async_run__mutmut_122": x_async_run__mutmut_122,
    "x_async_run__mutmut_123": x_async_run__mutmut_123,
    "x_async_run__mutmut_124": x_async_run__mutmut_124,
    "x_async_run__mutmut_125": x_async_run__mutmut_125,
    "x_async_run__mutmut_126": x_async_run__mutmut_126,
    "x_async_run__mutmut_127": x_async_run__mutmut_127,
    "x_async_run__mutmut_128": x_async_run__mutmut_128,
    "x_async_run__mutmut_129": x_async_run__mutmut_129,
}


def async_run(*args, **kwargs):
    result = _mutmut_trampoline(x_async_run__mutmut_orig, x_async_run__mutmut_mutants, args, kwargs)
    return result


async_run.__signature__ = _mutmut_signature(x_async_run__mutmut_orig)
x_async_run__mutmut_orig.__name__ = "x_async_run"


# <3 🧱🤝🏃🪄
