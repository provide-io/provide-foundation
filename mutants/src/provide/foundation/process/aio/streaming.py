# provide/foundation/process/aio/streaming.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import asyncio
import builtins
from collections.abc import AsyncIterator, Mapping
from pathlib import Path
from typing import Any

from provide.foundation.errors.process import ProcessError, ProcessTimeoutError
from provide.foundation.logger import get_logger
from provide.foundation.process.shared import filter_subprocess_kwargs, prepare_environment

"""Async subprocess streaming execution."""

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


async def x_create_stream_subprocess__mutmut_orig(
    cmd: list[str], cwd: str | None, run_env: dict[str, str], stream_stderr: bool, kwargs: dict[str, Any]
) -> Any:
    """Create subprocess for streaming.

    Args:
        cmd: Command to execute as list
        cwd: Working directory
        run_env: Environment variables
        stream_stderr: Whether to stream stderr to stdout
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    stderr_handling = asyncio.subprocess.STDOUT if stream_stderr else asyncio.subprocess.PIPE
    return await asyncio.create_subprocess_exec(
        *(cmd if isinstance(cmd, list) else cmd.split()),
        cwd=cwd,
        env=run_env,
        stdout=asyncio.subprocess.PIPE,
        stderr=stderr_handling,
        **filter_subprocess_kwargs(kwargs),
    )


async def x_create_stream_subprocess__mutmut_1(
    cmd: list[str], cwd: str | None, run_env: dict[str, str], stream_stderr: bool, kwargs: dict[str, Any]
) -> Any:
    """Create subprocess for streaming.

    Args:
        cmd: Command to execute as list
        cwd: Working directory
        run_env: Environment variables
        stream_stderr: Whether to stream stderr to stdout
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    stderr_handling = None
    return await asyncio.create_subprocess_exec(
        *(cmd if isinstance(cmd, list) else cmd.split()),
        cwd=cwd,
        env=run_env,
        stdout=asyncio.subprocess.PIPE,
        stderr=stderr_handling,
        **filter_subprocess_kwargs(kwargs),
    )


async def x_create_stream_subprocess__mutmut_2(
    cmd: list[str], cwd: str | None, run_env: dict[str, str], stream_stderr: bool, kwargs: dict[str, Any]
) -> Any:
    """Create subprocess for streaming.

    Args:
        cmd: Command to execute as list
        cwd: Working directory
        run_env: Environment variables
        stream_stderr: Whether to stream stderr to stdout
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    stderr_handling = asyncio.subprocess.STDOUT if stream_stderr else asyncio.subprocess.PIPE
    return await asyncio.create_subprocess_exec(
        *(cmd if isinstance(cmd, list) else cmd.split()),
        cwd=None,
        env=run_env,
        stdout=asyncio.subprocess.PIPE,
        stderr=stderr_handling,
        **filter_subprocess_kwargs(kwargs),
    )


async def x_create_stream_subprocess__mutmut_3(
    cmd: list[str], cwd: str | None, run_env: dict[str, str], stream_stderr: bool, kwargs: dict[str, Any]
) -> Any:
    """Create subprocess for streaming.

    Args:
        cmd: Command to execute as list
        cwd: Working directory
        run_env: Environment variables
        stream_stderr: Whether to stream stderr to stdout
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    stderr_handling = asyncio.subprocess.STDOUT if stream_stderr else asyncio.subprocess.PIPE
    return await asyncio.create_subprocess_exec(
        *(cmd if isinstance(cmd, list) else cmd.split()),
        cwd=cwd,
        env=None,
        stdout=asyncio.subprocess.PIPE,
        stderr=stderr_handling,
        **filter_subprocess_kwargs(kwargs),
    )


async def x_create_stream_subprocess__mutmut_4(
    cmd: list[str], cwd: str | None, run_env: dict[str, str], stream_stderr: bool, kwargs: dict[str, Any]
) -> Any:
    """Create subprocess for streaming.

    Args:
        cmd: Command to execute as list
        cwd: Working directory
        run_env: Environment variables
        stream_stderr: Whether to stream stderr to stdout
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    stderr_handling = asyncio.subprocess.STDOUT if stream_stderr else asyncio.subprocess.PIPE
    return await asyncio.create_subprocess_exec(
        *(cmd if isinstance(cmd, list) else cmd.split()),
        cwd=cwd,
        env=run_env,
        stdout=None,
        stderr=stderr_handling,
        **filter_subprocess_kwargs(kwargs),
    )


async def x_create_stream_subprocess__mutmut_5(
    cmd: list[str], cwd: str | None, run_env: dict[str, str], stream_stderr: bool, kwargs: dict[str, Any]
) -> Any:
    """Create subprocess for streaming.

    Args:
        cmd: Command to execute as list
        cwd: Working directory
        run_env: Environment variables
        stream_stderr: Whether to stream stderr to stdout
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    stderr_handling = asyncio.subprocess.STDOUT if stream_stderr else asyncio.subprocess.PIPE
    return await asyncio.create_subprocess_exec(
        *(cmd if isinstance(cmd, list) else cmd.split()),
        cwd=cwd,
        env=run_env,
        stdout=asyncio.subprocess.PIPE,
        stderr=None,
        **filter_subprocess_kwargs(kwargs),
    )


async def x_create_stream_subprocess__mutmut_6(
    cmd: list[str], cwd: str | None, run_env: dict[str, str], stream_stderr: bool, kwargs: dict[str, Any]
) -> Any:
    """Create subprocess for streaming.

    Args:
        cmd: Command to execute as list
        cwd: Working directory
        run_env: Environment variables
        stream_stderr: Whether to stream stderr to stdout
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    stderr_handling = asyncio.subprocess.STDOUT if stream_stderr else asyncio.subprocess.PIPE
    return await asyncio.create_subprocess_exec(
        cwd=cwd,
        env=run_env,
        stdout=asyncio.subprocess.PIPE,
        stderr=stderr_handling,
        **filter_subprocess_kwargs(kwargs),
    )


async def x_create_stream_subprocess__mutmut_7(
    cmd: list[str], cwd: str | None, run_env: dict[str, str], stream_stderr: bool, kwargs: dict[str, Any]
) -> Any:
    """Create subprocess for streaming.

    Args:
        cmd: Command to execute as list
        cwd: Working directory
        run_env: Environment variables
        stream_stderr: Whether to stream stderr to stdout
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    stderr_handling = asyncio.subprocess.STDOUT if stream_stderr else asyncio.subprocess.PIPE
    return await asyncio.create_subprocess_exec(
        *(cmd if isinstance(cmd, list) else cmd.split()),
        env=run_env,
        stdout=asyncio.subprocess.PIPE,
        stderr=stderr_handling,
        **filter_subprocess_kwargs(kwargs),
    )


async def x_create_stream_subprocess__mutmut_8(
    cmd: list[str], cwd: str | None, run_env: dict[str, str], stream_stderr: bool, kwargs: dict[str, Any]
) -> Any:
    """Create subprocess for streaming.

    Args:
        cmd: Command to execute as list
        cwd: Working directory
        run_env: Environment variables
        stream_stderr: Whether to stream stderr to stdout
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    stderr_handling = asyncio.subprocess.STDOUT if stream_stderr else asyncio.subprocess.PIPE
    return await asyncio.create_subprocess_exec(
        *(cmd if isinstance(cmd, list) else cmd.split()),
        cwd=cwd,
        stdout=asyncio.subprocess.PIPE,
        stderr=stderr_handling,
        **filter_subprocess_kwargs(kwargs),
    )


async def x_create_stream_subprocess__mutmut_9(
    cmd: list[str], cwd: str | None, run_env: dict[str, str], stream_stderr: bool, kwargs: dict[str, Any]
) -> Any:
    """Create subprocess for streaming.

    Args:
        cmd: Command to execute as list
        cwd: Working directory
        run_env: Environment variables
        stream_stderr: Whether to stream stderr to stdout
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    stderr_handling = asyncio.subprocess.STDOUT if stream_stderr else asyncio.subprocess.PIPE
    return await asyncio.create_subprocess_exec(
        *(cmd if isinstance(cmd, list) else cmd.split()),
        cwd=cwd,
        env=run_env,
        stderr=stderr_handling,
        **filter_subprocess_kwargs(kwargs),
    )


async def x_create_stream_subprocess__mutmut_10(
    cmd: list[str], cwd: str | None, run_env: dict[str, str], stream_stderr: bool, kwargs: dict[str, Any]
) -> Any:
    """Create subprocess for streaming.

    Args:
        cmd: Command to execute as list
        cwd: Working directory
        run_env: Environment variables
        stream_stderr: Whether to stream stderr to stdout
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    stderr_handling = asyncio.subprocess.STDOUT if stream_stderr else asyncio.subprocess.PIPE
    return await asyncio.create_subprocess_exec(
        *(cmd if isinstance(cmd, list) else cmd.split()),
        cwd=cwd,
        env=run_env,
        stdout=asyncio.subprocess.PIPE,
        **filter_subprocess_kwargs(kwargs),
    )


async def x_create_stream_subprocess__mutmut_11(
    cmd: list[str], cwd: str | None, run_env: dict[str, str], stream_stderr: bool, kwargs: dict[str, Any]
) -> Any:
    """Create subprocess for streaming.

    Args:
        cmd: Command to execute as list
        cwd: Working directory
        run_env: Environment variables
        stream_stderr: Whether to stream stderr to stdout
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    stderr_handling = asyncio.subprocess.STDOUT if stream_stderr else asyncio.subprocess.PIPE
    return await asyncio.create_subprocess_exec(
        *(cmd if isinstance(cmd, list) else cmd.split()),
        cwd=cwd,
        env=run_env,
        stdout=asyncio.subprocess.PIPE,
        stderr=stderr_handling,
        )


async def x_create_stream_subprocess__mutmut_12(
    cmd: list[str], cwd: str | None, run_env: dict[str, str], stream_stderr: bool, kwargs: dict[str, Any]
) -> Any:
    """Create subprocess for streaming.

    Args:
        cmd: Command to execute as list
        cwd: Working directory
        run_env: Environment variables
        stream_stderr: Whether to stream stderr to stdout
        kwargs: Additional subprocess parameters

    Returns:
        Created subprocess
    """
    stderr_handling = asyncio.subprocess.STDOUT if stream_stderr else asyncio.subprocess.PIPE
    return await asyncio.create_subprocess_exec(
        *(cmd if isinstance(cmd, list) else cmd.split()),
        cwd=cwd,
        env=run_env,
        stdout=asyncio.subprocess.PIPE,
        stderr=stderr_handling,
        **filter_subprocess_kwargs(None),
    )

x_create_stream_subprocess__mutmut_mutants : ClassVar[MutantDict] = {
'x_create_stream_subprocess__mutmut_1': x_create_stream_subprocess__mutmut_1, 
    'x_create_stream_subprocess__mutmut_2': x_create_stream_subprocess__mutmut_2, 
    'x_create_stream_subprocess__mutmut_3': x_create_stream_subprocess__mutmut_3, 
    'x_create_stream_subprocess__mutmut_4': x_create_stream_subprocess__mutmut_4, 
    'x_create_stream_subprocess__mutmut_5': x_create_stream_subprocess__mutmut_5, 
    'x_create_stream_subprocess__mutmut_6': x_create_stream_subprocess__mutmut_6, 
    'x_create_stream_subprocess__mutmut_7': x_create_stream_subprocess__mutmut_7, 
    'x_create_stream_subprocess__mutmut_8': x_create_stream_subprocess__mutmut_8, 
    'x_create_stream_subprocess__mutmut_9': x_create_stream_subprocess__mutmut_9, 
    'x_create_stream_subprocess__mutmut_10': x_create_stream_subprocess__mutmut_10, 
    'x_create_stream_subprocess__mutmut_11': x_create_stream_subprocess__mutmut_11, 
    'x_create_stream_subprocess__mutmut_12': x_create_stream_subprocess__mutmut_12
}

def create_stream_subprocess(*args, **kwargs):
    result = _mutmut_trampoline(x_create_stream_subprocess__mutmut_orig, x_create_stream_subprocess__mutmut_mutants, args, kwargs)
    return result 

create_stream_subprocess.__signature__ = _mutmut_signature(x_create_stream_subprocess__mutmut_orig)
x_create_stream_subprocess__mutmut_orig.__name__ = 'x_create_stream_subprocess'


async def x_read_lines_with_timeout__mutmut_orig(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_1(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = None
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_2(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_3(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = None
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_4(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = None

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_5(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while False:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_6(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = None
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_7(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() + start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_8(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = None

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_9(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout + elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_10(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout < 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_11(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 1:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_12(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = None

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_13(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                None,
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_14(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=None,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_15(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_16(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_17(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_18(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                return  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_19(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(None)
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_20(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").lstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_21(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors=None).rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_22(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="XXreplaceXX").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_23(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="REPLACE").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_24(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error(None, command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_25(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=None, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_26(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=None)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_27(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error(command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_28(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_29(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, )
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_30(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("XX⏱️ Async stream timed outXX", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_31(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_32(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ ASYNC STREAM TIMED OUT", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_33(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            None,
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_34(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code=None,
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_35(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=None,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_36(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=None,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_37(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_38(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_39(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_40(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_TIMEOUT",
            command=cmd_str,
            ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_41(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="XXPROCESS_ASYNC_STREAM_TIMEOUTXX",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines


async def x_read_lines_with_timeout__mutmut_42(process: Any, timeout: float, cmd_str: str) -> list[str]:
    """Read lines from process stdout with timeout.

    Args:
        process: Subprocess to read from
        timeout: Timeout in seconds
        cmd_str: Command string for error messages

    Returns:
        List of output lines

    Raises:
        ProcessTimeoutError: If timeout exceeded
    """
    lines: list[str] = []
    if not process.stdout:
        return lines

    try:
        remaining_timeout = timeout
        start_time = asyncio.get_event_loop().time()

        while True:
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining_timeout = timeout - elapsed

            if remaining_timeout <= 0:
                raise builtins.TimeoutError()

            # Wait for a line with remaining timeout
            line = await asyncio.wait_for(
                process.stdout.readline(),
                timeout=remaining_timeout,
            )

            if not line:
                break  # EOF

            lines.append(line.decode(errors="replace").rstrip())
    except builtins.TimeoutError as e:
        process.kill()
        await process.wait()
        log.error("⏱️ Async stream timed out", command=cmd_str, timeout=timeout)
        raise ProcessTimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="process_async_stream_timeout",
            command=cmd_str,
            timeout_seconds=timeout,
        ) from e

    return lines

x_read_lines_with_timeout__mutmut_mutants : ClassVar[MutantDict] = {
'x_read_lines_with_timeout__mutmut_1': x_read_lines_with_timeout__mutmut_1, 
    'x_read_lines_with_timeout__mutmut_2': x_read_lines_with_timeout__mutmut_2, 
    'x_read_lines_with_timeout__mutmut_3': x_read_lines_with_timeout__mutmut_3, 
    'x_read_lines_with_timeout__mutmut_4': x_read_lines_with_timeout__mutmut_4, 
    'x_read_lines_with_timeout__mutmut_5': x_read_lines_with_timeout__mutmut_5, 
    'x_read_lines_with_timeout__mutmut_6': x_read_lines_with_timeout__mutmut_6, 
    'x_read_lines_with_timeout__mutmut_7': x_read_lines_with_timeout__mutmut_7, 
    'x_read_lines_with_timeout__mutmut_8': x_read_lines_with_timeout__mutmut_8, 
    'x_read_lines_with_timeout__mutmut_9': x_read_lines_with_timeout__mutmut_9, 
    'x_read_lines_with_timeout__mutmut_10': x_read_lines_with_timeout__mutmut_10, 
    'x_read_lines_with_timeout__mutmut_11': x_read_lines_with_timeout__mutmut_11, 
    'x_read_lines_with_timeout__mutmut_12': x_read_lines_with_timeout__mutmut_12, 
    'x_read_lines_with_timeout__mutmut_13': x_read_lines_with_timeout__mutmut_13, 
    'x_read_lines_with_timeout__mutmut_14': x_read_lines_with_timeout__mutmut_14, 
    'x_read_lines_with_timeout__mutmut_15': x_read_lines_with_timeout__mutmut_15, 
    'x_read_lines_with_timeout__mutmut_16': x_read_lines_with_timeout__mutmut_16, 
    'x_read_lines_with_timeout__mutmut_17': x_read_lines_with_timeout__mutmut_17, 
    'x_read_lines_with_timeout__mutmut_18': x_read_lines_with_timeout__mutmut_18, 
    'x_read_lines_with_timeout__mutmut_19': x_read_lines_with_timeout__mutmut_19, 
    'x_read_lines_with_timeout__mutmut_20': x_read_lines_with_timeout__mutmut_20, 
    'x_read_lines_with_timeout__mutmut_21': x_read_lines_with_timeout__mutmut_21, 
    'x_read_lines_with_timeout__mutmut_22': x_read_lines_with_timeout__mutmut_22, 
    'x_read_lines_with_timeout__mutmut_23': x_read_lines_with_timeout__mutmut_23, 
    'x_read_lines_with_timeout__mutmut_24': x_read_lines_with_timeout__mutmut_24, 
    'x_read_lines_with_timeout__mutmut_25': x_read_lines_with_timeout__mutmut_25, 
    'x_read_lines_with_timeout__mutmut_26': x_read_lines_with_timeout__mutmut_26, 
    'x_read_lines_with_timeout__mutmut_27': x_read_lines_with_timeout__mutmut_27, 
    'x_read_lines_with_timeout__mutmut_28': x_read_lines_with_timeout__mutmut_28, 
    'x_read_lines_with_timeout__mutmut_29': x_read_lines_with_timeout__mutmut_29, 
    'x_read_lines_with_timeout__mutmut_30': x_read_lines_with_timeout__mutmut_30, 
    'x_read_lines_with_timeout__mutmut_31': x_read_lines_with_timeout__mutmut_31, 
    'x_read_lines_with_timeout__mutmut_32': x_read_lines_with_timeout__mutmut_32, 
    'x_read_lines_with_timeout__mutmut_33': x_read_lines_with_timeout__mutmut_33, 
    'x_read_lines_with_timeout__mutmut_34': x_read_lines_with_timeout__mutmut_34, 
    'x_read_lines_with_timeout__mutmut_35': x_read_lines_with_timeout__mutmut_35, 
    'x_read_lines_with_timeout__mutmut_36': x_read_lines_with_timeout__mutmut_36, 
    'x_read_lines_with_timeout__mutmut_37': x_read_lines_with_timeout__mutmut_37, 
    'x_read_lines_with_timeout__mutmut_38': x_read_lines_with_timeout__mutmut_38, 
    'x_read_lines_with_timeout__mutmut_39': x_read_lines_with_timeout__mutmut_39, 
    'x_read_lines_with_timeout__mutmut_40': x_read_lines_with_timeout__mutmut_40, 
    'x_read_lines_with_timeout__mutmut_41': x_read_lines_with_timeout__mutmut_41, 
    'x_read_lines_with_timeout__mutmut_42': x_read_lines_with_timeout__mutmut_42
}

def read_lines_with_timeout(*args, **kwargs):
    result = _mutmut_trampoline(x_read_lines_with_timeout__mutmut_orig, x_read_lines_with_timeout__mutmut_mutants, args, kwargs)
    return result 

read_lines_with_timeout.__signature__ = _mutmut_signature(x_read_lines_with_timeout__mutmut_orig)
x_read_lines_with_timeout__mutmut_orig.__name__ = 'x_read_lines_with_timeout'


async def x_cleanup_stream_process__mutmut_orig(process: Any) -> None:
    """Clean up subprocess resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist and are still open
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.STDOUT and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_stream_process__mutmut_1(process: Any) -> None:
    """Clean up subprocess resources.

    Args:
        process: Subprocess to clean up
    """
    if process:
        return

    # Close pipes if they exist and are still open
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.STDOUT and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_stream_process__mutmut_2(process: Any) -> None:
    """Clean up subprocess resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist and are still open
    if process.stdin or not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.STDOUT and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_stream_process__mutmut_3(process: Any) -> None:
    """Clean up subprocess resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist and are still open
    if process.stdin and process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.STDOUT and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_stream_process__mutmut_4(process: Any) -> None:
    """Clean up subprocess resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist and are still open
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout or not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.STDOUT and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_stream_process__mutmut_5(process: Any) -> None:
    """Clean up subprocess resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist and are still open
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.STDOUT and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_stream_process__mutmut_6(process: Any) -> None:
    """Clean up subprocess resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist and are still open
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.STDOUT or not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_stream_process__mutmut_7(process: Any) -> None:
    """Clean up subprocess resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist and are still open
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr or process.stderr != asyncio.subprocess.STDOUT and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_stream_process__mutmut_8(process: Any) -> None:
    """Clean up subprocess resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist and are still open
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr == asyncio.subprocess.STDOUT and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_stream_process__mutmut_9(process: Any) -> None:
    """Clean up subprocess resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist and are still open
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.STDOUT and process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_stream_process__mutmut_10(process: Any) -> None:
    """Clean up subprocess resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist and are still open
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.STDOUT and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is not None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_stream_process__mutmut_11(process: Any) -> None:
    """Clean up subprocess resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist and are still open
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.STDOUT and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(None, timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_stream_process__mutmut_12(process: Any) -> None:
    """Clean up subprocess resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist and are still open
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.STDOUT and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=None)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_stream_process__mutmut_13(process: Any) -> None:
    """Clean up subprocess resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist and are still open
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.STDOUT and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(timeout=1.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_stream_process__mutmut_14(process: Any) -> None:
    """Clean up subprocess resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist and are still open
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.STDOUT and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), )
        except builtins.TimeoutError:
            process.kill()
            await process.wait()


async def x_cleanup_stream_process__mutmut_15(process: Any) -> None:
    """Clean up subprocess resources.

    Args:
        process: Subprocess to clean up
    """
    if not process:
        return

    # Close pipes if they exist and are still open
    if process.stdin and not process.stdin.is_closing():
        process.stdin.close()
    if process.stdout and not process.stdout.at_eof():
        process.stdout.feed_eof()
    if process.stderr and process.stderr != asyncio.subprocess.STDOUT and not process.stderr.at_eof():
        process.stderr.feed_eof()

    # Ensure process is terminated
    if process.returncode is None:
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=2.0)
        except builtins.TimeoutError:
            process.kill()
            await process.wait()

x_cleanup_stream_process__mutmut_mutants : ClassVar[MutantDict] = {
'x_cleanup_stream_process__mutmut_1': x_cleanup_stream_process__mutmut_1, 
    'x_cleanup_stream_process__mutmut_2': x_cleanup_stream_process__mutmut_2, 
    'x_cleanup_stream_process__mutmut_3': x_cleanup_stream_process__mutmut_3, 
    'x_cleanup_stream_process__mutmut_4': x_cleanup_stream_process__mutmut_4, 
    'x_cleanup_stream_process__mutmut_5': x_cleanup_stream_process__mutmut_5, 
    'x_cleanup_stream_process__mutmut_6': x_cleanup_stream_process__mutmut_6, 
    'x_cleanup_stream_process__mutmut_7': x_cleanup_stream_process__mutmut_7, 
    'x_cleanup_stream_process__mutmut_8': x_cleanup_stream_process__mutmut_8, 
    'x_cleanup_stream_process__mutmut_9': x_cleanup_stream_process__mutmut_9, 
    'x_cleanup_stream_process__mutmut_10': x_cleanup_stream_process__mutmut_10, 
    'x_cleanup_stream_process__mutmut_11': x_cleanup_stream_process__mutmut_11, 
    'x_cleanup_stream_process__mutmut_12': x_cleanup_stream_process__mutmut_12, 
    'x_cleanup_stream_process__mutmut_13': x_cleanup_stream_process__mutmut_13, 
    'x_cleanup_stream_process__mutmut_14': x_cleanup_stream_process__mutmut_14, 
    'x_cleanup_stream_process__mutmut_15': x_cleanup_stream_process__mutmut_15
}

def cleanup_stream_process(*args, **kwargs):
    result = _mutmut_trampoline(x_cleanup_stream_process__mutmut_orig, x_cleanup_stream_process__mutmut_mutants, args, kwargs)
    return result 

cleanup_stream_process.__signature__ = _mutmut_signature(x_cleanup_stream_process__mutmut_orig)
x_cleanup_stream_process__mutmut_orig.__name__ = 'x_cleanup_stream_process'


def x_check_stream_exit_code__mutmut_orig(process: Any, cmd_str: str) -> None:
    """Check if process exited successfully.

    Args:
        process: Subprocess to check
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_FAILED",
            command=cmd_str,
            return_code=process.returncode,
        )


def x_check_stream_exit_code__mutmut_1(process: Any, cmd_str: str) -> None:
    """Check if process exited successfully.

    Args:
        process: Subprocess to check
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode == 0:
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_FAILED",
            command=cmd_str,
            return_code=process.returncode,
        )


def x_check_stream_exit_code__mutmut_2(process: Any, cmd_str: str) -> None:
    """Check if process exited successfully.

    Args:
        process: Subprocess to check
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 1:
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_FAILED",
            command=cmd_str,
            return_code=process.returncode,
        )


def x_check_stream_exit_code__mutmut_3(process: Any, cmd_str: str) -> None:
    """Check if process exited successfully.

    Args:
        process: Subprocess to check
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 0:
        raise ProcessError(
            None,
            code="PROCESS_ASYNC_STREAM_FAILED",
            command=cmd_str,
            return_code=process.returncode,
        )


def x_check_stream_exit_code__mutmut_4(process: Any, cmd_str: str) -> None:
    """Check if process exited successfully.

    Args:
        process: Subprocess to check
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code=None,
            command=cmd_str,
            return_code=process.returncode,
        )


def x_check_stream_exit_code__mutmut_5(process: Any, cmd_str: str) -> None:
    """Check if process exited successfully.

    Args:
        process: Subprocess to check
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_FAILED",
            command=None,
            return_code=process.returncode,
        )


def x_check_stream_exit_code__mutmut_6(process: Any, cmd_str: str) -> None:
    """Check if process exited successfully.

    Args:
        process: Subprocess to check
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_FAILED",
            command=cmd_str,
            return_code=None,
        )


def x_check_stream_exit_code__mutmut_7(process: Any, cmd_str: str) -> None:
    """Check if process exited successfully.

    Args:
        process: Subprocess to check
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 0:
        raise ProcessError(
            code="PROCESS_ASYNC_STREAM_FAILED",
            command=cmd_str,
            return_code=process.returncode,
        )


def x_check_stream_exit_code__mutmut_8(process: Any, cmd_str: str) -> None:
    """Check if process exited successfully.

    Args:
        process: Subprocess to check
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            command=cmd_str,
            return_code=process.returncode,
        )


def x_check_stream_exit_code__mutmut_9(process: Any, cmd_str: str) -> None:
    """Check if process exited successfully.

    Args:
        process: Subprocess to check
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_FAILED",
            return_code=process.returncode,
        )


def x_check_stream_exit_code__mutmut_10(process: Any, cmd_str: str) -> None:
    """Check if process exited successfully.

    Args:
        process: Subprocess to check
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_FAILED",
            command=cmd_str,
            )


def x_check_stream_exit_code__mutmut_11(process: Any, cmd_str: str) -> None:
    """Check if process exited successfully.

    Args:
        process: Subprocess to check
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="XXPROCESS_ASYNC_STREAM_FAILEDXX",
            command=cmd_str,
            return_code=process.returncode,
        )


def x_check_stream_exit_code__mutmut_12(process: Any, cmd_str: str) -> None:
    """Check if process exited successfully.

    Args:
        process: Subprocess to check
        cmd_str: Command string for error messages

    Raises:
        ProcessError: If process exited with non-zero code
    """
    if process.returncode != 0:
        raise ProcessError(
            f"Command failed with exit code {process.returncode}: {cmd_str}",
            code="process_async_stream_failed",
            command=cmd_str,
            return_code=process.returncode,
        )

x_check_stream_exit_code__mutmut_mutants : ClassVar[MutantDict] = {
'x_check_stream_exit_code__mutmut_1': x_check_stream_exit_code__mutmut_1, 
    'x_check_stream_exit_code__mutmut_2': x_check_stream_exit_code__mutmut_2, 
    'x_check_stream_exit_code__mutmut_3': x_check_stream_exit_code__mutmut_3, 
    'x_check_stream_exit_code__mutmut_4': x_check_stream_exit_code__mutmut_4, 
    'x_check_stream_exit_code__mutmut_5': x_check_stream_exit_code__mutmut_5, 
    'x_check_stream_exit_code__mutmut_6': x_check_stream_exit_code__mutmut_6, 
    'x_check_stream_exit_code__mutmut_7': x_check_stream_exit_code__mutmut_7, 
    'x_check_stream_exit_code__mutmut_8': x_check_stream_exit_code__mutmut_8, 
    'x_check_stream_exit_code__mutmut_9': x_check_stream_exit_code__mutmut_9, 
    'x_check_stream_exit_code__mutmut_10': x_check_stream_exit_code__mutmut_10, 
    'x_check_stream_exit_code__mutmut_11': x_check_stream_exit_code__mutmut_11, 
    'x_check_stream_exit_code__mutmut_12': x_check_stream_exit_code__mutmut_12
}

def check_stream_exit_code(*args, **kwargs):
    result = _mutmut_trampoline(x_check_stream_exit_code__mutmut_orig, x_check_stream_exit_code__mutmut_mutants, args, kwargs)
    return result 

check_stream_exit_code.__signature__ = _mutmut_signature(x_check_stream_exit_code__mutmut_orig)
x_check_stream_exit_code__mutmut_orig.__name__ = 'x_check_stream_exit_code'


async def x_async_stream__mutmut_orig(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_1(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = True,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_2(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = None
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_3(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(None) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_4(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = "XX XX".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_5(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(None)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_6(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info(None, command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_7(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=None, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_8(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_9(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info(command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_10(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_11(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, )

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_12(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("XX🌊 Streaming async commandXX", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_13(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_14(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 STREAMING ASYNC COMMAND", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_15(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(None) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_16(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = None
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_17(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(None)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_18(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = None

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_19(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(None) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_20(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = ""
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_21(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = None

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_22(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(None, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_23(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, None, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_24(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, None, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_25(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, None, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_26(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, None)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_27(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_28(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_29(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_30(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_31(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, )

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_32(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = None
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_33(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(None, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_34(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, None, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_35(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, None)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_36(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_37(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_38(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, )
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_39(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(None, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_40(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, None)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_41(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_42(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, )

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_43(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").lstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_44(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors=None).rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_45(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="XXreplaceXX").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_46(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="REPLACE").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_47(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(None, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_48(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, None)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_49(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_50(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, )

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_51(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug(None, command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_52(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=None)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_53(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug(command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_54(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", )
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_55(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("XX✅ Async stream completedXX", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_56(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_57(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ ASYNC STREAM COMPLETED", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_58(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(None)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_59(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error(None, command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_60(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=None, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_61(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=None)
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_62(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error(command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_63(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_64(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, )
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_65(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("XX💥 Async stream failedXX", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_66(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_67(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 ASYNC STREAM FAILED", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_68(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(None))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_69(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            None,
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_70(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code=None,
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_71(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=None,
        ) from e


async def x_async_stream__mutmut_72(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_73(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_74(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            ) from e


async def x_async_stream__mutmut_75(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="XXPROCESS_ASYNC_STREAM_ERRORXX",
            command=cmd_str,
        ) from e


async def x_async_stream__mutmut_76(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        stream_stderr: Whether to merge stderr into stdout
        **kwargs: Additional subprocess arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        ProcessTimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    log.info("🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment and working directory
    run_env = prepare_environment(env)
    cwd_str = str(cwd) if isinstance(cwd, Path) else cwd

    process = None
    try:
        # Create subprocess
        process = await create_stream_subprocess(cmd, cwd_str, run_env, stream_stderr, kwargs)

        try:
            # Stream output with optional timeout
            if timeout:
                lines = await read_lines_with_timeout(process, timeout, cmd_str)
                await process.wait()
                check_stream_exit_code(process, cmd_str)

                # Yield lines as they were read
                for line in lines:
                    yield line
            else:
                # No timeout - stream normally
                if process.stdout:
                    async for line in process.stdout:
                        yield line.decode(errors="replace").rstrip()

                # Wait for process to complete and check exit code
                await process.wait()
                check_stream_exit_code(process, cmd_str)

            log.debug("✅ Async stream completed", command=cmd_str)
        finally:
            await cleanup_stream_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | ProcessTimeoutError):
            raise

        log.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="process_async_stream_error",
            command=cmd_str,
        ) from e

x_async_stream__mutmut_mutants : ClassVar[MutantDict] = {
'x_async_stream__mutmut_1': x_async_stream__mutmut_1, 
    'x_async_stream__mutmut_2': x_async_stream__mutmut_2, 
    'x_async_stream__mutmut_3': x_async_stream__mutmut_3, 
    'x_async_stream__mutmut_4': x_async_stream__mutmut_4, 
    'x_async_stream__mutmut_5': x_async_stream__mutmut_5, 
    'x_async_stream__mutmut_6': x_async_stream__mutmut_6, 
    'x_async_stream__mutmut_7': x_async_stream__mutmut_7, 
    'x_async_stream__mutmut_8': x_async_stream__mutmut_8, 
    'x_async_stream__mutmut_9': x_async_stream__mutmut_9, 
    'x_async_stream__mutmut_10': x_async_stream__mutmut_10, 
    'x_async_stream__mutmut_11': x_async_stream__mutmut_11, 
    'x_async_stream__mutmut_12': x_async_stream__mutmut_12, 
    'x_async_stream__mutmut_13': x_async_stream__mutmut_13, 
    'x_async_stream__mutmut_14': x_async_stream__mutmut_14, 
    'x_async_stream__mutmut_15': x_async_stream__mutmut_15, 
    'x_async_stream__mutmut_16': x_async_stream__mutmut_16, 
    'x_async_stream__mutmut_17': x_async_stream__mutmut_17, 
    'x_async_stream__mutmut_18': x_async_stream__mutmut_18, 
    'x_async_stream__mutmut_19': x_async_stream__mutmut_19, 
    'x_async_stream__mutmut_20': x_async_stream__mutmut_20, 
    'x_async_stream__mutmut_21': x_async_stream__mutmut_21, 
    'x_async_stream__mutmut_22': x_async_stream__mutmut_22, 
    'x_async_stream__mutmut_23': x_async_stream__mutmut_23, 
    'x_async_stream__mutmut_24': x_async_stream__mutmut_24, 
    'x_async_stream__mutmut_25': x_async_stream__mutmut_25, 
    'x_async_stream__mutmut_26': x_async_stream__mutmut_26, 
    'x_async_stream__mutmut_27': x_async_stream__mutmut_27, 
    'x_async_stream__mutmut_28': x_async_stream__mutmut_28, 
    'x_async_stream__mutmut_29': x_async_stream__mutmut_29, 
    'x_async_stream__mutmut_30': x_async_stream__mutmut_30, 
    'x_async_stream__mutmut_31': x_async_stream__mutmut_31, 
    'x_async_stream__mutmut_32': x_async_stream__mutmut_32, 
    'x_async_stream__mutmut_33': x_async_stream__mutmut_33, 
    'x_async_stream__mutmut_34': x_async_stream__mutmut_34, 
    'x_async_stream__mutmut_35': x_async_stream__mutmut_35, 
    'x_async_stream__mutmut_36': x_async_stream__mutmut_36, 
    'x_async_stream__mutmut_37': x_async_stream__mutmut_37, 
    'x_async_stream__mutmut_38': x_async_stream__mutmut_38, 
    'x_async_stream__mutmut_39': x_async_stream__mutmut_39, 
    'x_async_stream__mutmut_40': x_async_stream__mutmut_40, 
    'x_async_stream__mutmut_41': x_async_stream__mutmut_41, 
    'x_async_stream__mutmut_42': x_async_stream__mutmut_42, 
    'x_async_stream__mutmut_43': x_async_stream__mutmut_43, 
    'x_async_stream__mutmut_44': x_async_stream__mutmut_44, 
    'x_async_stream__mutmut_45': x_async_stream__mutmut_45, 
    'x_async_stream__mutmut_46': x_async_stream__mutmut_46, 
    'x_async_stream__mutmut_47': x_async_stream__mutmut_47, 
    'x_async_stream__mutmut_48': x_async_stream__mutmut_48, 
    'x_async_stream__mutmut_49': x_async_stream__mutmut_49, 
    'x_async_stream__mutmut_50': x_async_stream__mutmut_50, 
    'x_async_stream__mutmut_51': x_async_stream__mutmut_51, 
    'x_async_stream__mutmut_52': x_async_stream__mutmut_52, 
    'x_async_stream__mutmut_53': x_async_stream__mutmut_53, 
    'x_async_stream__mutmut_54': x_async_stream__mutmut_54, 
    'x_async_stream__mutmut_55': x_async_stream__mutmut_55, 
    'x_async_stream__mutmut_56': x_async_stream__mutmut_56, 
    'x_async_stream__mutmut_57': x_async_stream__mutmut_57, 
    'x_async_stream__mutmut_58': x_async_stream__mutmut_58, 
    'x_async_stream__mutmut_59': x_async_stream__mutmut_59, 
    'x_async_stream__mutmut_60': x_async_stream__mutmut_60, 
    'x_async_stream__mutmut_61': x_async_stream__mutmut_61, 
    'x_async_stream__mutmut_62': x_async_stream__mutmut_62, 
    'x_async_stream__mutmut_63': x_async_stream__mutmut_63, 
    'x_async_stream__mutmut_64': x_async_stream__mutmut_64, 
    'x_async_stream__mutmut_65': x_async_stream__mutmut_65, 
    'x_async_stream__mutmut_66': x_async_stream__mutmut_66, 
    'x_async_stream__mutmut_67': x_async_stream__mutmut_67, 
    'x_async_stream__mutmut_68': x_async_stream__mutmut_68, 
    'x_async_stream__mutmut_69': x_async_stream__mutmut_69, 
    'x_async_stream__mutmut_70': x_async_stream__mutmut_70, 
    'x_async_stream__mutmut_71': x_async_stream__mutmut_71, 
    'x_async_stream__mutmut_72': x_async_stream__mutmut_72, 
    'x_async_stream__mutmut_73': x_async_stream__mutmut_73, 
    'x_async_stream__mutmut_74': x_async_stream__mutmut_74, 
    'x_async_stream__mutmut_75': x_async_stream__mutmut_75, 
    'x_async_stream__mutmut_76': x_async_stream__mutmut_76
}

def async_stream(*args, **kwargs):
    result = _mutmut_trampoline(x_async_stream__mutmut_orig, x_async_stream__mutmut_mutants, args, kwargs)
    return result 

async_stream.__signature__ = _mutmut_signature(x_async_stream__mutmut_orig)
x_async_stream__mutmut_orig.__name__ = 'x_async_stream'


# <3 🧱🤝🏃🪄
