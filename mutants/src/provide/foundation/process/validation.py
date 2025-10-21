# provide/foundation/process/validation.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

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


class ShellFeatureError(ProcessError):
    """Raised when shell features are used without explicit permission."""

    def xǁShellFeatureErrorǁ__init____mutmut_orig(self, message: str, pattern: str, command: str) -> None:
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

    def xǁShellFeatureErrorǁ__init____mutmut_1(self, message: str, pattern: str, command: str) -> None:
        """Initialize ShellFeatureError.

        Args:
            message: Error message
            pattern: The dangerous pattern detected
            command: The command that contained the pattern

        """
        # Truncate command for safety
        truncated_command = None

        super().__init__(
            message,
            code="SHELL_FEATURE_NOT_ALLOWED",
            pattern=pattern,
            command=truncated_command,
        )
        self.pattern = pattern
        self.command = truncated_command

    def xǁShellFeatureErrorǁ__init____mutmut_2(self, message: str, pattern: str, command: str) -> None:
        """Initialize ShellFeatureError.

        Args:
            message: Error message
            pattern: The dangerous pattern detected
            command: The command that contained the pattern

        """
        # Truncate command for safety
        truncated_command = command[:101]

        super().__init__(
            message,
            code="SHELL_FEATURE_NOT_ALLOWED",
            pattern=pattern,
            command=truncated_command,
        )
        self.pattern = pattern
        self.command = truncated_command

    def xǁShellFeatureErrorǁ__init____mutmut_3(self, message: str, pattern: str, command: str) -> None:
        """Initialize ShellFeatureError.

        Args:
            message: Error message
            pattern: The dangerous pattern detected
            command: The command that contained the pattern

        """
        # Truncate command for safety
        truncated_command = command[:100]

        super().__init__(
            None,
            code="SHELL_FEATURE_NOT_ALLOWED",
            pattern=pattern,
            command=truncated_command,
        )
        self.pattern = pattern
        self.command = truncated_command

    def xǁShellFeatureErrorǁ__init____mutmut_4(self, message: str, pattern: str, command: str) -> None:
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
            code=None,
            pattern=pattern,
            command=truncated_command,
        )
        self.pattern = pattern
        self.command = truncated_command

    def xǁShellFeatureErrorǁ__init____mutmut_5(self, message: str, pattern: str, command: str) -> None:
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
            pattern=None,
            command=truncated_command,
        )
        self.pattern = pattern
        self.command = truncated_command

    def xǁShellFeatureErrorǁ__init____mutmut_6(self, message: str, pattern: str, command: str) -> None:
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
            command=None,
        )
        self.pattern = pattern
        self.command = truncated_command

    def xǁShellFeatureErrorǁ__init____mutmut_7(self, message: str, pattern: str, command: str) -> None:
        """Initialize ShellFeatureError.

        Args:
            message: Error message
            pattern: The dangerous pattern detected
            command: The command that contained the pattern

        """
        # Truncate command for safety
        truncated_command = command[:100]

        super().__init__(
            code="SHELL_FEATURE_NOT_ALLOWED",
            pattern=pattern,
            command=truncated_command,
        )
        self.pattern = pattern
        self.command = truncated_command

    def xǁShellFeatureErrorǁ__init____mutmut_8(self, message: str, pattern: str, command: str) -> None:
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
            pattern=pattern,
            command=truncated_command,
        )
        self.pattern = pattern
        self.command = truncated_command

    def xǁShellFeatureErrorǁ__init____mutmut_9(self, message: str, pattern: str, command: str) -> None:
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
            command=truncated_command,
        )
        self.pattern = pattern
        self.command = truncated_command

    def xǁShellFeatureErrorǁ__init____mutmut_10(self, message: str, pattern: str, command: str) -> None:
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
            )
        self.pattern = pattern
        self.command = truncated_command

    def xǁShellFeatureErrorǁ__init____mutmut_11(self, message: str, pattern: str, command: str) -> None:
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
            code="XXSHELL_FEATURE_NOT_ALLOWEDXX",
            pattern=pattern,
            command=truncated_command,
        )
        self.pattern = pattern
        self.command = truncated_command

    def xǁShellFeatureErrorǁ__init____mutmut_12(self, message: str, pattern: str, command: str) -> None:
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
            code="shell_feature_not_allowed",
            pattern=pattern,
            command=truncated_command,
        )
        self.pattern = pattern
        self.command = truncated_command

    def xǁShellFeatureErrorǁ__init____mutmut_13(self, message: str, pattern: str, command: str) -> None:
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
        self.pattern = None
        self.command = truncated_command

    def xǁShellFeatureErrorǁ__init____mutmut_14(self, message: str, pattern: str, command: str) -> None:
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
        self.command = None
    
    xǁShellFeatureErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁShellFeatureErrorǁ__init____mutmut_1': xǁShellFeatureErrorǁ__init____mutmut_1, 
        'xǁShellFeatureErrorǁ__init____mutmut_2': xǁShellFeatureErrorǁ__init____mutmut_2, 
        'xǁShellFeatureErrorǁ__init____mutmut_3': xǁShellFeatureErrorǁ__init____mutmut_3, 
        'xǁShellFeatureErrorǁ__init____mutmut_4': xǁShellFeatureErrorǁ__init____mutmut_4, 
        'xǁShellFeatureErrorǁ__init____mutmut_5': xǁShellFeatureErrorǁ__init____mutmut_5, 
        'xǁShellFeatureErrorǁ__init____mutmut_6': xǁShellFeatureErrorǁ__init____mutmut_6, 
        'xǁShellFeatureErrorǁ__init____mutmut_7': xǁShellFeatureErrorǁ__init____mutmut_7, 
        'xǁShellFeatureErrorǁ__init____mutmut_8': xǁShellFeatureErrorǁ__init____mutmut_8, 
        'xǁShellFeatureErrorǁ__init____mutmut_9': xǁShellFeatureErrorǁ__init____mutmut_9, 
        'xǁShellFeatureErrorǁ__init____mutmut_10': xǁShellFeatureErrorǁ__init____mutmut_10, 
        'xǁShellFeatureErrorǁ__init____mutmut_11': xǁShellFeatureErrorǁ__init____mutmut_11, 
        'xǁShellFeatureErrorǁ__init____mutmut_12': xǁShellFeatureErrorǁ__init____mutmut_12, 
        'xǁShellFeatureErrorǁ__init____mutmut_13': xǁShellFeatureErrorǁ__init____mutmut_13, 
        'xǁShellFeatureErrorǁ__init____mutmut_14': xǁShellFeatureErrorǁ__init____mutmut_14
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁShellFeatureErrorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁShellFeatureErrorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁShellFeatureErrorǁ__init____mutmut_orig)
    xǁShellFeatureErrorǁ__init____mutmut_orig.__name__ = 'xǁShellFeatureErrorǁ__init__'


def x_validate_shell_safety__mutmut_orig(cmd: str, allow_shell_features: bool = False) -> None:
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


def x_validate_shell_safety__mutmut_1(cmd: str, allow_shell_features: bool = True) -> None:
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


def x_validate_shell_safety__mutmut_2(cmd: str, allow_shell_features: bool = False) -> None:
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
        if pattern not in cmd:
            raise ShellFeatureError(
                f"Shell feature '{pattern}' detected in command. "
                f"Use allow_shell_features=True to explicitly enable shell features, "
                f"or use run() with a list of arguments for safer execution.",
                pattern=pattern,
                command=cmd,
            )


def x_validate_shell_safety__mutmut_3(cmd: str, allow_shell_features: bool = False) -> None:
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
                None,
                pattern=pattern,
                command=cmd,
            )


def x_validate_shell_safety__mutmut_4(cmd: str, allow_shell_features: bool = False) -> None:
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
                pattern=None,
                command=cmd,
            )


def x_validate_shell_safety__mutmut_5(cmd: str, allow_shell_features: bool = False) -> None:
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
                command=None,
            )


def x_validate_shell_safety__mutmut_6(cmd: str, allow_shell_features: bool = False) -> None:
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
                pattern=pattern,
                command=cmd,
            )


def x_validate_shell_safety__mutmut_7(cmd: str, allow_shell_features: bool = False) -> None:
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
                command=cmd,
            )


def x_validate_shell_safety__mutmut_8(cmd: str, allow_shell_features: bool = False) -> None:
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
                )

x_validate_shell_safety__mutmut_mutants : ClassVar[MutantDict] = {
'x_validate_shell_safety__mutmut_1': x_validate_shell_safety__mutmut_1, 
    'x_validate_shell_safety__mutmut_2': x_validate_shell_safety__mutmut_2, 
    'x_validate_shell_safety__mutmut_3': x_validate_shell_safety__mutmut_3, 
    'x_validate_shell_safety__mutmut_4': x_validate_shell_safety__mutmut_4, 
    'x_validate_shell_safety__mutmut_5': x_validate_shell_safety__mutmut_5, 
    'x_validate_shell_safety__mutmut_6': x_validate_shell_safety__mutmut_6, 
    'x_validate_shell_safety__mutmut_7': x_validate_shell_safety__mutmut_7, 
    'x_validate_shell_safety__mutmut_8': x_validate_shell_safety__mutmut_8
}

def validate_shell_safety(*args, **kwargs):
    result = _mutmut_trampoline(x_validate_shell_safety__mutmut_orig, x_validate_shell_safety__mutmut_mutants, args, kwargs)
    return result 

validate_shell_safety.__signature__ = _mutmut_signature(x_validate_shell_safety__mutmut_orig)
x_validate_shell_safety__mutmut_orig.__name__ = 'x_validate_shell_safety'


__all__ = [
    "DANGEROUS_SHELL_PATTERNS",
    "ShellFeatureError",
    "validate_shell_safety",
]


# <3 🧱🤝🏃🪄
