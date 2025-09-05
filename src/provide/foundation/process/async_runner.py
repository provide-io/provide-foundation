"""Async subprocess execution utilities."""

import asyncio
import builtins
from collections.abc import AsyncIterator, Mapping
import os
from pathlib import Path
from typing import Any

from provide.foundation.logger import get_logger
from provide.foundation.process.runner import (
    CompletedProcess,
    ProcessError,
    TimeoutError,
)

plog = get_logger(__name__)


async def async_run_command(
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
    """
    Run a subprocess command asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        input: Input to send to the process
        **kwargs: Additional arguments

    Returns:
        CompletedProcess with results

    Raises:
        ProcessError: If command fails and check=True
        TimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    plog.info(
        "🚀 Running async command", command=cmd_str, cwd=str(cwd) if cwd else None
    )

    # Prepare environment
    run_env = dict(env) if env is not None else os.environ.copy()

    # Convert Path to string
    if isinstance(cwd, Path):
        cwd = str(cwd)

    try:
        # Create subprocess
        if shell:
            # For shell commands, use create_subprocess_shell with string command
            process = await asyncio.create_subprocess_shell(
                cmd_str,
                cwd=cwd,
                env=run_env,
                stdout=asyncio.subprocess.PIPE if capture_output else None,
                stderr=asyncio.subprocess.PIPE if capture_output else None,
                stdin=asyncio.subprocess.PIPE if input else None,
                **{k: v for k, v in kwargs.items() if k != 'shell'},
            )
        else:
            # For non-shell commands, use create_subprocess_exec with unpacked args
            process = await asyncio.create_subprocess_exec(
                *(cmd if isinstance(cmd, list) else [cmd]),
                cwd=cwd,
                env=run_env,
                stdout=asyncio.subprocess.PIPE if capture_output else None,
                stderr=asyncio.subprocess.PIPE if capture_output else None,
                stdin=asyncio.subprocess.PIPE if input else None,
                **{k: v for k, v in kwargs.items() if k != 'shell'},
            )

        # Communicate with process
        if timeout:
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(input=input),
                    timeout=timeout,
                )
            except builtins.TimeoutError:
                process.kill()
                await process.wait()
                plog.error(
                    "⏱️ Async command timed out", command=cmd_str, timeout=timeout
                )
                raise TimeoutError(
                    f"Command timed out after {timeout}s: {cmd_str}",
                    code="PROCESS_ASYNC_TIMEOUT",
                    command=cmd_str,
                    timeout=timeout,
                )
        else:
            stdout, stderr = await process.communicate(input=input)

        # Decode output
        stdout_str = stdout.decode() if stdout else ""
        stderr_str = stderr.decode() if stderr else ""

        completed = CompletedProcess(
            args=cmd,
            returncode=process.returncode or 0,
            stdout=stdout_str,
            stderr=stderr_str,
            cwd=cwd,
            env=dict(run_env) if env else None,
        )

        if check and process.returncode != 0:
            plog.error(
                "❌ Async command failed",
                command=cmd_str,
                returncode=process.returncode,
                stderr=stderr_str if capture_output else None,
            )
            raise ProcessError(
                f"Command failed with exit code {process.returncode}: {cmd_str}",
                code="PROCESS_ASYNC_FAILED",
                command=cmd_str,
                returncode=process.returncode,
                stdout=stdout_str if capture_output else None,
                stderr=stderr_str if capture_output else None,
            )

        plog.debug(
            "✅ Async command completed",
            command=cmd_str,
            returncode=process.returncode,
        )

        return completed

    except Exception as e:
        if isinstance(e, ProcessError | TimeoutError):
            raise

        plog.error(
            "💥 Async command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute async command: {cmd_str}",
            code="PROCESS_ASYNC_EXECUTION_FAILED",
            command=cmd_str,
            error=str(e),
        ) from e


async def async_stream_command(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> AsyncIterator[str]:
    """
    Stream command output line by line asynchronously.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        **kwargs: Additional arguments

    Yields:
        Lines of output from the command

    Raises:
        ProcessError: If command fails
        TimeoutError: If timeout is exceeded
    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    plog.info(
        "🌊 Streaming async command", command=cmd_str, cwd=str(cwd) if cwd else None
    )

    # Prepare environment
    run_env = dict(env) if env is not None else os.environ.copy()

    # Convert Path to string
    if isinstance(cwd, Path):
        cwd = str(cwd)

    try:
        # Create subprocess
        # Merge stderr to stdout for streaming, as we always want to see errors
        stderr_handling = asyncio.subprocess.STDOUT
        process = await asyncio.create_subprocess_exec(
            *(cmd if isinstance(cmd, list) else [cmd]),
            cwd=cwd,
            env=run_env,
            stdout=asyncio.subprocess.PIPE,
            stderr=stderr_handling,
            **kwargs,
        )

        # Stream output with optional timeout
        if timeout:
            # For timeout, we need to handle it differently
            # Create a task to read lines with timeout
            async def read_with_timeout():
                lines = []
                if process.stdout:
                    try:
                        # Use wait_for on each readline operation
                        remaining_timeout = timeout
                        start_time = asyncio.get_event_loop().time()
                        
                        while True:
                            elapsed = asyncio.get_event_loop().time() - start_time
                            remaining_timeout = timeout - elapsed
                            
                            if remaining_timeout <= 0:
                                raise asyncio.TimeoutError()
                            
                            # Wait for a line with remaining timeout
                            line = await asyncio.wait_for(
                                process.stdout.readline(), 
                                timeout=remaining_timeout
                            )
                            
                            if not line:
                                break  # EOF
                            
                            lines.append(line.decode().rstrip())
                    except asyncio.TimeoutError:
                        process.kill()
                        await process.wait()
                        plog.error(
                            "⏱️ Async stream timed out", command=cmd_str, timeout=timeout
                        )
                        raise TimeoutError(
                            f"Command timed out after {timeout}s: {cmd_str}",
                            code="PROCESS_ASYNC_STREAM_TIMEOUT",
                            command=cmd_str,
                            timeout=timeout,
                        )
                
                # Wait for process to complete
                await process.wait()
                
                if process.returncode != 0:
                    raise ProcessError(
                        f"Command failed with exit code {process.returncode}: {cmd_str}",
                        code="PROCESS_ASYNC_STREAM_FAILED",
                        command=cmd_str,
                        returncode=process.returncode,
                    )
                
                return lines
            
            # Yield lines as they were read
            lines = await read_with_timeout()
            for line in lines:
                yield line
        else:
            # No timeout - stream normally
            if process.stdout:
                async for line in process.stdout:
                    yield line.decode().rstrip()
            
            # Wait for process to complete
            await process.wait()
            
            if process.returncode != 0:
                raise ProcessError(
                    f"Command failed with exit code {process.returncode}: {cmd_str}",
                    code="PROCESS_ASYNC_STREAM_FAILED",
                    command=cmd_str,
                    returncode=process.returncode,
                )

        plog.debug("✅ Async stream completed", command=cmd_str)

    except Exception as e:
        if isinstance(e, ProcessError | TimeoutError):
            raise

        plog.error("💥 Async stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream async command: {cmd_str}",
            code="PROCESS_ASYNC_STREAM_ERROR",
            command=cmd_str,
            error=str(e),
        ) from e


async def async_run_shell(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command asynchronously.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results
    """
    return await async_run_command(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,
        **kwargs,
    )
