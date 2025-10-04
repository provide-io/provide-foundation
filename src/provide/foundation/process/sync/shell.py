from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from provide.foundation.errors.config import ValidationError
from provide.foundation.logger import get_logger
from provide.foundation.process.shared import CompletedProcess
from provide.foundation.process.sync.execution import run

"""Shell command execution wrapper."""

plog = get_logger(__name__)


def shell(
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
        Use run() with a list for safer execution.

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Basic validation - log warning for potentially dangerous patterns
    dangerous_patterns = [";", "&&", "||", "|", ">", "<", "&", "$", "`"]
    if any(pattern in cmd for pattern in dangerous_patterns):
        plog.warning("Shell command contains potentially dangerous characters", command=cmd)

    return run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )
