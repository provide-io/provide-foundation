#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from provide.foundation.errors.config import ValidationError
from provide.foundation.process.aio.execution import async_run
from provide.foundation.process.defaults import DEFAULT_SHELL_ALLOW_FEATURES
from provide.foundation.process.shared import CompletedProcess
from provide.foundation.process.validation import validate_shell_safety

"""Shell command execution via async subprocess."""


async def async_shell(
    cmd: str,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    capture_output: bool = True,
    check: bool = True,
    timeout: float | None = None,
    allow_shell_features: bool = DEFAULT_SHELL_ALLOW_FEATURES,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a shell command asynchronously with safety validation.

    WARNING: This function uses shell=True. By default, shell metacharacters
    are DENIED to prevent command injection. Use allow_shell_features=True
    only with trusted input.

    Args:
        cmd: Shell command string
        cwd: Working directory
        env: Environment variables
        capture_output: Whether to capture output
        check: Whether to raise on non-zero exit
        timeout: Command timeout in seconds
        allow_shell_features: Allow shell metacharacters (default: False)
        **kwargs: Additional subprocess arguments

    Returns:
        CompletedProcess with results

    Raises:
        ValidationError: If cmd is not a string
        ShellFeatureError: If shell features used without explicit permission

    Security Note:
        For maximum security, use async_run() with a list of arguments instead.
        Only set allow_shell_features=True if you fully trust the command source.

        Safe:   await async_shell("ls -la", allow_shell_features=False)  # OK
        Unsafe: await async_shell(user_input)  # Will raise ShellFeatureError if metacharacters present
        Risky:  await async_shell(user_input, allow_shell_features=True)  # DO NOT DO THIS

    """
    if not isinstance(cmd, str):
        raise ValidationError(
            "Shell command must be a string",
            code="INVALID_SHELL_COMMAND",
            expected_type="str",
            actual_type=type(cmd).__name__,
        )

    # Validate shell safety - raises ShellFeatureError if dangerous patterns found
    validate_shell_safety(cmd, allow_shell_features=allow_shell_features)

    return await async_run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=capture_output,
        check=check,
        timeout=timeout,
        shell=True,  # nosec B604 - Intentional shell usage with validation
        **kwargs,
    )


# 🧱🏗️🔚
