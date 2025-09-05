"""Core subprocess execution utilities."""

from collections.abc import Iterator, Mapping
import os
from pathlib import Path
import subprocess
from typing import Any

from attrs import define

from provide.foundation.errors.integration import TimeoutError
from provide.foundation.errors.runtime import ProcessError
from provide.foundation.logger import get_logger

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
    """
    Run a subprocess command with consistent error handling and logging.

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
        if shell:
            # For shell commands, ensure it's a string
            subprocess_cmd = cmd_str
        else:
            # For non-shell, use the original cmd (list or string)
            subprocess_cmd = cmd

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
            shell=shell,
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
    """
    Simple wrapper for run_command that returns stdout as a string.

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


def stream_command(
    cmd: list[str],
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    stream_stderr: bool = False,
    **kwargs: Any,
) -> Iterator[str]:
    """
    Stream command output line by line.

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
    import fcntl
    import os
    import select
    import time

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    plog.info("🌊 Streaming command", command=cmd_str, cwd=str(cwd) if cwd else None)

    # Prepare environment, disabling foundation telemetry by default
    run_env = os.environ.copy()
    if env is not None:
        run_env.update(env)
    run_env.setdefault("PROVIDE_TELEMETRY_DISABLED", "true")

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

        if timeout is not None:
            start_time = time.time()

            if process.stdout:
                # Use non-blocking I/O with timeout
                # Make stdout non-blocking
                fd = process.stdout.fileno()
                fl = fcntl.fcntl(fd, fcntl.F_GETFL)
                fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

                buffer = ""
                while True:
                    elapsed = time.time() - start_time
                    if elapsed >= timeout:
                        process.kill()
                        process.wait()
                        plog.error(
                            "⏱️ Stream timed out", command=cmd_str, timeout=timeout
                        )
                        raise TimeoutError(
                            f"Command timed out after {timeout}s: {cmd_str}",
                            code="PROCESS_STREAM_TIMEOUT",
                            command=cmd_str,
                            timeout=timeout,
                        )

                    # Use select with timeout
                    remaining = timeout - elapsed
                    ready, _, _ = select.select(
                        [process.stdout], [], [], min(0.1, remaining)
                    )

                    if ready:
                        try:
                            chunk = process.stdout.read(1024)
                            if not chunk:
                                break  # EOF
                            buffer += chunk

                            # Yield complete lines
                            while "\n" in buffer:
                                line, buffer = buffer.split("\n", 1)
                                yield line.rstrip()
                        except OSError:
                            # No data available yet
                            pass

                    # Check if process ended
                    if process.poll() is not None:
                        # Read any remaining data
                        remaining_data = process.stdout.read()
                        if remaining_data:
                            buffer += remaining_data

                        # Yield any remaining lines
                        for line in buffer.split("\n"):
                            if line:
                                yield line.rstrip()
                        break

                # Wait for process to complete
                returncode = process.poll()
                if returncode is None:
                    returncode = process.wait()
        else:
            # No timeout - use blocking I/O
            if process.stdout:
                for line in process.stdout:
                    yield line.rstrip()

            # Wait for process to complete
            returncode = process.wait()

        if returncode != 0:
            raise ProcessError(
                f"Command failed with exit code {returncode}: {cmd_str}",
                code="PROCESS_STREAM_FAILED",
                command=cmd_str,
                returncode=returncode,
            )

        plog.debug("✅ Stream completed", command=cmd_str)
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
    return run_command(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,
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
