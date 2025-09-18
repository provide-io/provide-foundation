from __future__ import annotations

from collections.abc import Iterator, Mapping
import os
from pathlib import Path
import subprocess
from typing import Any

from attrs import define

from provide.foundation.errors.integration import TimeoutError
from provide.foundation.errors.runtime import ProcessError
from provide.foundation.logger import get_logger

"""Core subprocess execution utilities."""

plog = get_logger(__name__)


@define
class CompletedProcess:
    """Result of a completed process."""

    args: list[str]
    returncode: int
    stdout: str
    stderr: str
    cwd: str | None = None
    env: dict[str, str] | None = None


def run_command(
    cmd: list[str] | str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    text: bool = True,
    input: str | bytes | None = None,
    shell: bool = False,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a subprocess command with consistent error handling and logging.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        env: Environment variables (if None, uses current environment)
        capture_output: Whether to capture stdout/stderr
        check: Whether to raise exception on non-zero exit
        timeout: Command timeout in seconds
        text: Whether to decode output as text
        input: Input to send to the process
        shell: Whether to run command through shell
        **kwargs: Additional arguments passed to subprocess.run

    Returns:
        CompletedProcess with results

    Raises:
        ProcessError: If command fails and check=True
        TimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    plog.info("🚀 Running command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment, disabling foundation telemetry by default
    run_env = os.environ.copy()
    if env is not None:
        run_env.update(env)
    run_env.setdefault("PROVIDE_TELEMETRY_DISABLED", "true")

    # Convert Path to string
    if isinstance(cwd, Path):
        cwd = str(cwd)

    # If command is a string, we need shell=True
    if isinstance(cmd, str) and not shell:
        shell = True

    try:
        # Prepare command for subprocess
        subprocess_cmd = cmd_str if shell else cmd

        # Handle input based on text mode
        if input is not None and text and isinstance(input, bytes):
            # Convert bytes to string if text mode is enabled
            subprocess_input = input.decode("utf-8")
        elif input is not None and not text and isinstance(input, str):
            # Convert string to bytes if text mode is disabled
            subprocess_input = input.encode("utf-8")
        else:
            subprocess_input = input

        result = subprocess.run(
            subprocess_cmd,
            cwd=cwd,
            env=run_env,
            capture_output=capture_output,
            text=text,
            input=subprocess_input,
            timeout=timeout,
            check=False,  # We'll handle the check ourselves
            shell=shell,  # nosec B602 - Shell usage validated by caller context
            **kwargs,
        )

        completed = CompletedProcess(
            args=cmd if isinstance(cmd, list) else [cmd],
            returncode=result.returncode,
            stdout=result.stdout if capture_output else "",
            stderr=result.stderr if capture_output else "",
            cwd=cwd,
            env=dict(run_env) if env else None,
        )

        if check and result.returncode != 0:
            plog.error(
                "❌ Command failed",
                command=cmd_str,
                returncode=result.returncode,
                stderr=result.stderr if capture_output else None,
            )
            raise ProcessError(
                f"Command failed with exit code {result.returncode}: {cmd_str}",
                code="PROCESS_COMMAND_FAILED",
                command=cmd_str,
                returncode=result.returncode,
                stdout=result.stdout if capture_output else None,
                stderr=result.stderr if capture_output else None,
            )

        plog.debug(
            "✅ Command completed",
            command=cmd_str,
            returncode=result.returncode,
        )

        return completed

    except subprocess.TimeoutExpired as e:
        plog.error(
            "⏱️ Command timed out",
            command=cmd_str,
            timeout=timeout,
        )
        raise TimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_TIMEOUT",
            command=cmd_str,
            timeout=timeout,
        ) from e
    except Exception as e:
        if isinstance(e, ProcessError | TimeoutError):
            raise
        plog.error(
            "💥 Command execution failed",
            command=cmd_str,
            error=str(e),
        )
        raise ProcessError(
            f"Failed to execute command: {cmd_str}",
            code="PROCESS_EXECUTION_FAILED",
            command=cmd_str,
            error=str(e),
        ) from e


def run_command_simple(
    cmd: list[str],
    cwd: str | Path | None = None,
    **kwargs: Any,
) -> str:
    """Simple wrapper for run_command that returns stdout as a string.

    Args:
        cmd: Command and arguments as a list
        cwd: Working directory for the command
        **kwargs: Additional arguments passed to run_command

    Returns:
        Stdout as a stripped string

    Raises:
        ProcessError: If command fails

    """
    result = run_command(cmd, cwd=cwd, capture_output=True, check=True, **kwargs)
    return result.stdout.strip()


def _setup_stream_environment(env: Mapping[str, str] | None) -> dict[str, str]:
    """Setup environment for streaming commands."""
    run_env = os.environ.copy()
    if env is not None:
        run_env.update(env)
    run_env.setdefault("PROVIDE_TELEMETRY_DISABLED", "true")
    return run_env


def _make_stdout_nonblocking(stdout: Any) -> None:
    """Make stdout non-blocking for timeout handling."""
    import fcntl
    import os

    fd = stdout.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)


def _check_timeout_expired(start_time: float, timeout: float, cmd_str: str, process: Any) -> None:
    """Check if timeout has expired and handle it."""
    import time

    elapsed = time.time() - start_time
    if elapsed >= timeout:
        process.kill()
        process.wait()
        plog.error("⏱️ Stream timed out", command=cmd_str, timeout=timeout)
        raise TimeoutError(
            f"Command timed out after {timeout}s: {cmd_str}",
            code="PROCESS_STREAM_TIMEOUT",
            command=cmd_str,
            timeout=timeout,
        )


def _read_chunk_from_stdout(stdout: Any, buffer: str) -> tuple[str, bool]:
    """Read a chunk from stdout and update buffer. Returns (new_buffer, eof_reached)."""
    try:
        chunk = stdout.read(1024)
        if not chunk:
            return buffer, True  # EOF
        return buffer + chunk, False
    except OSError:
        # No data available yet
        return buffer, False


def _yield_complete_lines(buffer: str) -> Iterator[tuple[str, str]]:
    """Yield complete lines from buffer. Returns (line, remaining_buffer) tuples."""
    while "\n" in buffer:
        line, buffer = buffer.split("\n", 1)
        yield line.rstrip(), buffer


def _yield_remaining_lines(buffer: str) -> Iterator[str]:
    """Yield any remaining lines from buffer."""
    for line in buffer.split("\n"):
        if line:
            yield line.rstrip()


def _finalize_remaining_data(stdout: Any, buffer: str) -> Iterator[str]:
    """Read any remaining data and yield final lines."""
    remaining_data = stdout.read()
    if remaining_data:
        buffer += remaining_data

    yield from _yield_remaining_lines(buffer)


def _stream_with_timeout(process: Any, timeout: float, cmd_str: str) -> Iterator[str]:
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


def _stream_without_timeout(process: Any) -> Iterator[str]:
    """Stream output without timeout (blocking I/O)."""
    if process.stdout:
        for line in process.stdout:
            yield line.rstrip()


def _cleanup_process(process: Any) -> None:
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


def stream_command(
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
        TimeoutError: If timeout is exceeded

    """
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    plog.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    run_env = _setup_stream_environment(env)

    # Convert Path to string
    if isinstance(cwd, Path):
        cwd = str(cwd)

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
                    returncode=returncode,
                )

            plog.debug("✅ Stream completed", command=cmd_str)
        finally:
            _cleanup_process(process)

    except Exception as e:
        if isinstance(e, ProcessError | TimeoutError):
            raise
        plog.error("💥 Stream failed", command=cmd_str, error=str(e))
        raise ProcessError(
            f"Failed to stream command: {cmd_str}",
            code="PROCESS_STREAM_ERROR",
            command=cmd_str,
            error=str(e),
        ) from e


def run_shell(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command.

    WARNING: This function uses shell=True, which can be dangerous with
    unsanitized input. Only use with trusted commands or properly sanitized input.

    Args:
        cmd: Shell command string (MUST be trusted/sanitized)
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Security Note:
        This function enables shell interpretation of the command string,
        which allows shell features but also creates injection risks.
        Use run_command with a list for safer execution.

    """
    if not isinstance(cmd, str):
        raise TypeError("Shell command must be a string")

    # Basic validation - log warning for potentially dangerous patterns
    dangerous_patterns = [";", "&&", "||", "|", ">", "<", "&", "$", "`"]
    if any(pattern in cmd for pattern in dangerous_patterns):
        plog.warning("Shell command contains potentially dangerous characters", command=cmd)

    return run_command(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


# Export all public functions
__all__ = [
    "CompletedProcess",
    "run_command",
    "run_command_simple",
    "run_shell",
    "stream_command",
]
