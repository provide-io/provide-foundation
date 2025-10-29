# provide/foundation/security/masking.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import re

from provide.foundation.security.defaults import DEFAULT_SECRET_PATTERNS, MASKED_VALUE

"""Secret masking utilities for command execution and sensitive strings."""
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


def x_mask_secrets__mutmut_orig(
    text: str,
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in text using regex patterns.

    Args:
        text: Text to mask secrets in
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Text with secrets masked

    """
    if secret_patterns is None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    result = text
    for pattern in secret_patterns:
        # Pattern should have 2 groups: (prefix)(secret_value)
        # We keep the prefix and mask the value
        result = re.sub(
            pattern,
            lambda m: f"{m.group(1)}{masked}",
            result,
            flags=re.IGNORECASE,
        )

    return result


def x_mask_secrets__mutmut_1(
    text: str,
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in text using regex patterns.

    Args:
        text: Text to mask secrets in
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Text with secrets masked

    """
    if secret_patterns is not None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    result = text
    for pattern in secret_patterns:
        # Pattern should have 2 groups: (prefix)(secret_value)
        # We keep the prefix and mask the value
        result = re.sub(
            pattern,
            lambda m: f"{m.group(1)}{masked}",
            result,
            flags=re.IGNORECASE,
        )

    return result


def x_mask_secrets__mutmut_2(
    text: str,
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in text using regex patterns.

    Args:
        text: Text to mask secrets in
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Text with secrets masked

    """
    if secret_patterns is None:
        secret_patterns = None

    result = text
    for pattern in secret_patterns:
        # Pattern should have 2 groups: (prefix)(secret_value)
        # We keep the prefix and mask the value
        result = re.sub(
            pattern,
            lambda m: f"{m.group(1)}{masked}",
            result,
            flags=re.IGNORECASE,
        )

    return result


def x_mask_secrets__mutmut_3(
    text: str,
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in text using regex patterns.

    Args:
        text: Text to mask secrets in
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Text with secrets masked

    """
    if secret_patterns is None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    result = None
    for pattern in secret_patterns:
        # Pattern should have 2 groups: (prefix)(secret_value)
        # We keep the prefix and mask the value
        result = re.sub(
            pattern,
            lambda m: f"{m.group(1)}{masked}",
            result,
            flags=re.IGNORECASE,
        )

    return result


def x_mask_secrets__mutmut_4(
    text: str,
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in text using regex patterns.

    Args:
        text: Text to mask secrets in
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Text with secrets masked

    """
    if secret_patterns is None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    result = text
    for pattern in secret_patterns:
        # Pattern should have 2 groups: (prefix)(secret_value)
        # We keep the prefix and mask the value
        result = None

    return result


def x_mask_secrets__mutmut_5(
    text: str,
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in text using regex patterns.

    Args:
        text: Text to mask secrets in
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Text with secrets masked

    """
    if secret_patterns is None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    result = text
    for pattern in secret_patterns:
        # Pattern should have 2 groups: (prefix)(secret_value)
        # We keep the prefix and mask the value
        result = re.sub(
            None,
            lambda m: f"{m.group(1)}{masked}",
            result,
            flags=re.IGNORECASE,
        )

    return result


def x_mask_secrets__mutmut_6(
    text: str,
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in text using regex patterns.

    Args:
        text: Text to mask secrets in
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Text with secrets masked

    """
    if secret_patterns is None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    result = text
    for pattern in secret_patterns:
        # Pattern should have 2 groups: (prefix)(secret_value)
        # We keep the prefix and mask the value
        result = re.sub(
            pattern,
            None,
            result,
            flags=re.IGNORECASE,
        )

    return result


def x_mask_secrets__mutmut_7(
    text: str,
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in text using regex patterns.

    Args:
        text: Text to mask secrets in
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Text with secrets masked

    """
    if secret_patterns is None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    result = text
    for pattern in secret_patterns:
        # Pattern should have 2 groups: (prefix)(secret_value)
        # We keep the prefix and mask the value
        result = re.sub(
            pattern,
            lambda m: f"{m.group(1)}{masked}",
            None,
            flags=re.IGNORECASE,
        )

    return result


def x_mask_secrets__mutmut_8(
    text: str,
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in text using regex patterns.

    Args:
        text: Text to mask secrets in
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Text with secrets masked

    """
    if secret_patterns is None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    result = text
    for pattern in secret_patterns:
        # Pattern should have 2 groups: (prefix)(secret_value)
        # We keep the prefix and mask the value
        result = re.sub(
            pattern,
            lambda m: f"{m.group(1)}{masked}",
            result,
            flags=None,
        )

    return result


def x_mask_secrets__mutmut_9(
    text: str,
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in text using regex patterns.

    Args:
        text: Text to mask secrets in
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Text with secrets masked

    """
    if secret_patterns is None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    result = text
    for pattern in secret_patterns:
        # Pattern should have 2 groups: (prefix)(secret_value)
        # We keep the prefix and mask the value
        result = re.sub(
            lambda m: f"{m.group(1)}{masked}",
            result,
            flags=re.IGNORECASE,
        )

    return result


def x_mask_secrets__mutmut_10(
    text: str,
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in text using regex patterns.

    Args:
        text: Text to mask secrets in
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Text with secrets masked

    """
    if secret_patterns is None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    result = text
    for pattern in secret_patterns:
        # Pattern should have 2 groups: (prefix)(secret_value)
        # We keep the prefix and mask the value
        result = re.sub(
            pattern,
            result,
            flags=re.IGNORECASE,
        )

    return result


def x_mask_secrets__mutmut_11(
    text: str,
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in text using regex patterns.

    Args:
        text: Text to mask secrets in
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Text with secrets masked

    """
    if secret_patterns is None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    result = text
    for pattern in secret_patterns:
        # Pattern should have 2 groups: (prefix)(secret_value)
        # We keep the prefix and mask the value
        result = re.sub(
            pattern,
            lambda m: f"{m.group(1)}{masked}",
            flags=re.IGNORECASE,
        )

    return result


def x_mask_secrets__mutmut_12(
    text: str,
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in text using regex patterns.

    Args:
        text: Text to mask secrets in
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Text with secrets masked

    """
    if secret_patterns is None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    result = text
    for pattern in secret_patterns:
        # Pattern should have 2 groups: (prefix)(secret_value)
        # We keep the prefix and mask the value
        result = re.sub(
            pattern,
            lambda m: f"{m.group(1)}{masked}",
            result,
        )

    return result


def x_mask_secrets__mutmut_13(
    text: str,
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in text using regex patterns.

    Args:
        text: Text to mask secrets in
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Text with secrets masked

    """
    if secret_patterns is None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    result = text
    for pattern in secret_patterns:
        # Pattern should have 2 groups: (prefix)(secret_value)
        # We keep the prefix and mask the value
        result = re.sub(
            pattern,
            lambda m: None,
            result,
            flags=re.IGNORECASE,
        )

    return result


def x_mask_secrets__mutmut_14(
    text: str,
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in text using regex patterns.

    Args:
        text: Text to mask secrets in
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Text with secrets masked

    """
    if secret_patterns is None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    result = text
    for pattern in secret_patterns:
        # Pattern should have 2 groups: (prefix)(secret_value)
        # We keep the prefix and mask the value
        result = re.sub(
            pattern,
            lambda m: f"{m.group(None)}{masked}",
            result,
            flags=re.IGNORECASE,
        )

    return result


def x_mask_secrets__mutmut_15(
    text: str,
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in text using regex patterns.

    Args:
        text: Text to mask secrets in
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Text with secrets masked

    """
    if secret_patterns is None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    result = text
    for pattern in secret_patterns:
        # Pattern should have 2 groups: (prefix)(secret_value)
        # We keep the prefix and mask the value
        result = re.sub(
            pattern,
            lambda m: f"{m.group(2)}{masked}",
            result,
            flags=re.IGNORECASE,
        )

    return result


x_mask_secrets__mutmut_mutants: ClassVar[MutantDict] = {
    "x_mask_secrets__mutmut_1": x_mask_secrets__mutmut_1,
    "x_mask_secrets__mutmut_2": x_mask_secrets__mutmut_2,
    "x_mask_secrets__mutmut_3": x_mask_secrets__mutmut_3,
    "x_mask_secrets__mutmut_4": x_mask_secrets__mutmut_4,
    "x_mask_secrets__mutmut_5": x_mask_secrets__mutmut_5,
    "x_mask_secrets__mutmut_6": x_mask_secrets__mutmut_6,
    "x_mask_secrets__mutmut_7": x_mask_secrets__mutmut_7,
    "x_mask_secrets__mutmut_8": x_mask_secrets__mutmut_8,
    "x_mask_secrets__mutmut_9": x_mask_secrets__mutmut_9,
    "x_mask_secrets__mutmut_10": x_mask_secrets__mutmut_10,
    "x_mask_secrets__mutmut_11": x_mask_secrets__mutmut_11,
    "x_mask_secrets__mutmut_12": x_mask_secrets__mutmut_12,
    "x_mask_secrets__mutmut_13": x_mask_secrets__mutmut_13,
    "x_mask_secrets__mutmut_14": x_mask_secrets__mutmut_14,
    "x_mask_secrets__mutmut_15": x_mask_secrets__mutmut_15,
}


def mask_secrets(*args, **kwargs):
    result = _mutmut_trampoline(x_mask_secrets__mutmut_orig, x_mask_secrets__mutmut_mutants, args, kwargs)
    return result


mask_secrets.__signature__ = _mutmut_signature(x_mask_secrets__mutmut_orig)
x_mask_secrets__mutmut_orig.__name__ = "x_mask_secrets"


def x_mask_command__mutmut_orig(
    cmd: str | list[str],
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in command for safe logging.

    Args:
        cmd: Command string or list to mask
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Command string with secrets masked

    """
    # Convert to string if list
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd

    return mask_secrets(cmd_str, secret_patterns, masked)


def x_mask_command__mutmut_1(
    cmd: str | list[str],
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in command for safe logging.

    Args:
        cmd: Command string or list to mask
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Command string with secrets masked

    """
    # Convert to string if list
    cmd_str = None

    return mask_secrets(cmd_str, secret_patterns, masked)


def x_mask_command__mutmut_2(
    cmd: str | list[str],
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in command for safe logging.

    Args:
        cmd: Command string or list to mask
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Command string with secrets masked

    """
    # Convert to string if list
    cmd_str = " ".join(None) if isinstance(cmd, list) else cmd

    return mask_secrets(cmd_str, secret_patterns, masked)


def x_mask_command__mutmut_3(
    cmd: str | list[str],
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in command for safe logging.

    Args:
        cmd: Command string or list to mask
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Command string with secrets masked

    """
    # Convert to string if list
    cmd_str = "XX XX".join(cmd) if isinstance(cmd, list) else cmd

    return mask_secrets(cmd_str, secret_patterns, masked)


def x_mask_command__mutmut_4(
    cmd: str | list[str],
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in command for safe logging.

    Args:
        cmd: Command string or list to mask
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Command string with secrets masked

    """
    # Convert to string if list
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd

    return mask_secrets(None, secret_patterns, masked)


def x_mask_command__mutmut_5(
    cmd: str | list[str],
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in command for safe logging.

    Args:
        cmd: Command string or list to mask
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Command string with secrets masked

    """
    # Convert to string if list
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd

    return mask_secrets(cmd_str, None, masked)


def x_mask_command__mutmut_6(
    cmd: str | list[str],
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in command for safe logging.

    Args:
        cmd: Command string or list to mask
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Command string with secrets masked

    """
    # Convert to string if list
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd

    return mask_secrets(cmd_str, secret_patterns, None)


def x_mask_command__mutmut_7(
    cmd: str | list[str],
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in command for safe logging.

    Args:
        cmd: Command string or list to mask
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Command string with secrets masked

    """
    # Convert to string if list
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd

    return mask_secrets(secret_patterns, masked)


def x_mask_command__mutmut_8(
    cmd: str | list[str],
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in command for safe logging.

    Args:
        cmd: Command string or list to mask
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Command string with secrets masked

    """
    # Convert to string if list
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd

    return mask_secrets(cmd_str, masked)


def x_mask_command__mutmut_9(
    cmd: str | list[str],
    secret_patterns: list[str] | None = None,
    masked: str = MASKED_VALUE,
) -> str:
    """Mask secrets in command for safe logging.

    Args:
        cmd: Command string or list to mask
        secret_patterns: List of regex patterns to match secrets
        masked: Replacement value for matched secrets

    Returns:
        Command string with secrets masked

    """
    # Convert to string if list
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd

    return mask_secrets(
        cmd_str,
        secret_patterns,
    )


x_mask_command__mutmut_mutants: ClassVar[MutantDict] = {
    "x_mask_command__mutmut_1": x_mask_command__mutmut_1,
    "x_mask_command__mutmut_2": x_mask_command__mutmut_2,
    "x_mask_command__mutmut_3": x_mask_command__mutmut_3,
    "x_mask_command__mutmut_4": x_mask_command__mutmut_4,
    "x_mask_command__mutmut_5": x_mask_command__mutmut_5,
    "x_mask_command__mutmut_6": x_mask_command__mutmut_6,
    "x_mask_command__mutmut_7": x_mask_command__mutmut_7,
    "x_mask_command__mutmut_8": x_mask_command__mutmut_8,
    "x_mask_command__mutmut_9": x_mask_command__mutmut_9,
}


def mask_command(*args, **kwargs):
    result = _mutmut_trampoline(x_mask_command__mutmut_orig, x_mask_command__mutmut_mutants, args, kwargs)
    return result


mask_command.__signature__ = _mutmut_signature(x_mask_command__mutmut_orig)
x_mask_command__mutmut_orig.__name__ = "x_mask_command"


def x_should_mask__mutmut_orig(text: str, secret_patterns: list[str] | None = None) -> bool:
    """Check if text contains secrets that should be masked.

    Args:
        text: Text to check
        secret_patterns: List of regex patterns to match secrets

    Returns:
        True if text contains secrets

    """
    if secret_patterns is None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in secret_patterns)


def x_should_mask__mutmut_1(text: str, secret_patterns: list[str] | None = None) -> bool:
    """Check if text contains secrets that should be masked.

    Args:
        text: Text to check
        secret_patterns: List of regex patterns to match secrets

    Returns:
        True if text contains secrets

    """
    if secret_patterns is not None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in secret_patterns)


def x_should_mask__mutmut_2(text: str, secret_patterns: list[str] | None = None) -> bool:
    """Check if text contains secrets that should be masked.

    Args:
        text: Text to check
        secret_patterns: List of regex patterns to match secrets

    Returns:
        True if text contains secrets

    """
    if secret_patterns is None:
        secret_patterns = None

    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in secret_patterns)


def x_should_mask__mutmut_3(text: str, secret_patterns: list[str] | None = None) -> bool:
    """Check if text contains secrets that should be masked.

    Args:
        text: Text to check
        secret_patterns: List of regex patterns to match secrets

    Returns:
        True if text contains secrets

    """
    if secret_patterns is None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    return any(None)


def x_should_mask__mutmut_4(text: str, secret_patterns: list[str] | None = None) -> bool:
    """Check if text contains secrets that should be masked.

    Args:
        text: Text to check
        secret_patterns: List of regex patterns to match secrets

    Returns:
        True if text contains secrets

    """
    if secret_patterns is None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    return any(re.search(None, text, flags=re.IGNORECASE) for pattern in secret_patterns)


def x_should_mask__mutmut_5(text: str, secret_patterns: list[str] | None = None) -> bool:
    """Check if text contains secrets that should be masked.

    Args:
        text: Text to check
        secret_patterns: List of regex patterns to match secrets

    Returns:
        True if text contains secrets

    """
    if secret_patterns is None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    return any(re.search(pattern, None, flags=re.IGNORECASE) for pattern in secret_patterns)


def x_should_mask__mutmut_6(text: str, secret_patterns: list[str] | None = None) -> bool:
    """Check if text contains secrets that should be masked.

    Args:
        text: Text to check
        secret_patterns: List of regex patterns to match secrets

    Returns:
        True if text contains secrets

    """
    if secret_patterns is None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    return any(re.search(pattern, text, flags=None) for pattern in secret_patterns)


def x_should_mask__mutmut_7(text: str, secret_patterns: list[str] | None = None) -> bool:
    """Check if text contains secrets that should be masked.

    Args:
        text: Text to check
        secret_patterns: List of regex patterns to match secrets

    Returns:
        True if text contains secrets

    """
    if secret_patterns is None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    return any(re.search(text, flags=re.IGNORECASE) for pattern in secret_patterns)


def x_should_mask__mutmut_8(text: str, secret_patterns: list[str] | None = None) -> bool:
    """Check if text contains secrets that should be masked.

    Args:
        text: Text to check
        secret_patterns: List of regex patterns to match secrets

    Returns:
        True if text contains secrets

    """
    if secret_patterns is None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    return any(re.search(pattern, flags=re.IGNORECASE) for pattern in secret_patterns)


def x_should_mask__mutmut_9(text: str, secret_patterns: list[str] | None = None) -> bool:
    """Check if text contains secrets that should be masked.

    Args:
        text: Text to check
        secret_patterns: List of regex patterns to match secrets

    Returns:
        True if text contains secrets

    """
    if secret_patterns is None:
        secret_patterns = DEFAULT_SECRET_PATTERNS

    return any(
        re.search(
            pattern,
            text,
        )
        for pattern in secret_patterns
    )


x_should_mask__mutmut_mutants: ClassVar[MutantDict] = {
    "x_should_mask__mutmut_1": x_should_mask__mutmut_1,
    "x_should_mask__mutmut_2": x_should_mask__mutmut_2,
    "x_should_mask__mutmut_3": x_should_mask__mutmut_3,
    "x_should_mask__mutmut_4": x_should_mask__mutmut_4,
    "x_should_mask__mutmut_5": x_should_mask__mutmut_5,
    "x_should_mask__mutmut_6": x_should_mask__mutmut_6,
    "x_should_mask__mutmut_7": x_should_mask__mutmut_7,
    "x_should_mask__mutmut_8": x_should_mask__mutmut_8,
    "x_should_mask__mutmut_9": x_should_mask__mutmut_9,
}


def should_mask(*args, **kwargs):
    result = _mutmut_trampoline(x_should_mask__mutmut_orig, x_should_mask__mutmut_mutants, args, kwargs)
    return result


should_mask.__signature__ = _mutmut_signature(x_should_mask__mutmut_orig)
x_should_mask__mutmut_orig.__name__ = "x_should_mask"


__all__ = [
    "DEFAULT_SECRET_PATTERNS",
    "MASKED_VALUE",
    "mask_command",
    "mask_secrets",
    "should_mask",
]


# <3 🧱🤝🛡️🪄
