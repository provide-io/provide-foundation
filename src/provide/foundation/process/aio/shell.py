from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from provide.foundation.process.aio.execution import async_run
from provide.foundation.process.shared import CompletedProcess

"""Shell command execution via async subprocess."""


async def async_shell(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command asynchronously.

    WARNING: This function uses shell=True, which can be dangerous with
    unsanitized input. Only use with trusted commands or properly sanitized input.

    Args:
        cmd: Shell command string (MUST be trusted/sanitized)
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout in seconds
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Security Note:
        This function enables shell interpretation of the command string,
        which allows shell features but also creates injection risks.
        Use async_run() with a list for safer execution.
    """
    return await async_run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with caller validation
        **kwargs,
    )
