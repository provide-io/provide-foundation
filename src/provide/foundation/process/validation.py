#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from provide.foundation.errors.process import ProcessError

"""Process command validation and safety checks."""

# Shell metacharacters that enable command injection or unintended behavior
DANGEROUS_SHELL_PATTERNS = [
    ";",  # Command chaining
    "&&",  # Conditional execution
    "||",  # Conditional execution
    "|",  # Piping
    ">",  # Output redirection
    "<",  # Input redirection
    "&",  # Background execution
    "$",  # Variable expansion
    "`",  # Command substitution
    "(",  # Subshell
    ")",  # Subshell
    "{",  # Brace expansion
    "}",  # Brace expansion
    "*",  # Glob expansion
    "?",  # Glob expansion
    "~",  # Tilde expansion
    "\n",  # Newline injection
    "\r",  # Carriage return injection
]


class ShellFeatureError(ProcessError):
    """Raised when shell features are used without explicit permission."""

    def __init__(self, message: str, pattern: str, command: str) -> None:
        """Initialize ShellFeatureError.

        Args:
            message: Error message
            pattern: The dangerous pattern detected
            command: The command that contained the pattern

        """
        # Truncate command for safety
        truncated_command = command[:100]

        super().__init__(
            message,
            code="SHELL_FEATURE_NOT_ALLOWED",
            pattern=pattern,
            command=truncated_command,
        )
        self.pattern = pattern
        self.command = truncated_command


def validate_shell_safety(cmd: str, allow_shell_features: bool = False) -> None:
    """Validate command string for shell injection risks.

    This function checks for dangerous shell metacharacters that could enable
    command injection or unintended behavior. By default, these features are
    denied to prevent security vulnerabilities.

    Args:
        cmd: Command string to validate
        allow_shell_features: If True, allow shell metacharacters (default: False)

    Raises:
        ShellFeatureError: If dangerous patterns found and not explicitly allowed

    Security Note:
        Only set allow_shell_features=True if you:
        1. Trust the source of the command string
        2. Have properly sanitized/validated the input
        3. Understand the security implications
        4. Need shell features like pipes, redirection, or variable expansion

        For most use cases, use run() with a list of arguments instead.

    Examples:
        >>> validate_shell_safety("ls -la")  # OK - no shell features
        >>> validate_shell_safety("cat file.txt | grep pattern")  # Raises ShellFeatureError
        >>> validate_shell_safety("cat file.txt | grep pattern", allow_shell_features=True)  # OK
    """
    if allow_shell_features:
        # User has explicitly opted in to shell features
        return

    # Check for dangerous patterns
    for pattern in DANGEROUS_SHELL_PATTERNS:
        if pattern in cmd:
            raise ShellFeatureError(
                f"Shell feature '{pattern}' detected in command. "
                f"Use allow_shell_features=True to explicitly enable shell features, "
                f"or use run() with a list of arguments for safer execution.",
                pattern=pattern,
                command=cmd,
            )


__all__ = [
    "DANGEROUS_SHELL_PATTERNS",
    "ShellFeatureError",
    "validate_shell_safety",
]

# 🧱🏗️🔚
