# provide/foundation/process/env.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from collections.abc import Mapping
import os

from provide.foundation.process.defaults import DEFAULT_ENV_SCRUBBING_ENABLED

"""Environment variable handling and scrubbing for subprocess execution."""

# Safe environment variables that can be passed to subprocesses
# These are common, non-sensitive environment variables
SAFE_ENV_ALLOWLIST = {
    # System paths
    "PATH",
    "HOME",
    "TMPDIR",
    "TEMP",
    "TMP",
    # Locale and language
    "LANG",
    "LANGUAGE",
    "LC_ALL",
    "LC_CTYPE",
    "LC_MESSAGES",
    # Terminal
    "TERM",
    "COLORTERM",
    # Python-specific (safe)
    "PYTHONPATH",
    "PYTHONHASHSEED",
    "PYTHONDONTWRITEBYTECODE",
    "PYTHONUNBUFFERED",
    # User info (generally safe)
    "USER",
    "USERNAME",
    "LOGNAME",
    # Display
    "DISPLAY",
    # Common safe variables
    "SHELL",
    "EDITOR",
    "PAGER",
    # Foundation-specific
    "PROVIDE_TELEMETRY_DISABLED",
    "PROVIDE_LOG_LEVEL",
    "PROVIDE_LOG_FORMAT",
    # CI/CD indicators (safe, non-secret)
    "CI",
    "GITHUB_ACTIONS",
    "GITLAB_CI",
    "JENKINS_HOME",
    # Platform identifiers
    "OS",
    "OSTYPE",
}

# Sensitive patterns in environment variable names
SENSITIVE_ENV_PATTERNS = [
    "TOKEN",
    "SECRET",
    "KEY",
    "PASSWORD",
    "PASSWD",
    "API_KEY",
    "APIKEY",
    "AUTH",
    "CREDENTIAL",
    "AWS_ACCESS_KEY",
    "AWS_SECRET",
    "GCP_KEY",
    "AZURE_",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GITHUB_TOKEN",
    "GITLAB_TOKEN",
    "NPM_TOKEN",
    "PYPI_TOKEN",
    "DOCKER_PASSWORD",
    "DATABASE_URL",
    "DB_PASS",
    "PRIVATE_KEY",
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


def x_is_sensitive_env_var__mutmut_orig(name: str) -> bool:
    """Check if environment variable name indicates sensitive data.

    Args:
        name: Environment variable name

    Returns:
        True if the name suggests sensitive data

    """
    name_upper = name.upper()
    return any(pattern in name_upper for pattern in SENSITIVE_ENV_PATTERNS)


def x_is_sensitive_env_var__mutmut_1(name: str) -> bool:
    """Check if environment variable name indicates sensitive data.

    Args:
        name: Environment variable name

    Returns:
        True if the name suggests sensitive data

    """
    name_upper = None
    return any(pattern in name_upper for pattern in SENSITIVE_ENV_PATTERNS)


def x_is_sensitive_env_var__mutmut_2(name: str) -> bool:
    """Check if environment variable name indicates sensitive data.

    Args:
        name: Environment variable name

    Returns:
        True if the name suggests sensitive data

    """
    name_upper = name.lower()
    return any(pattern in name_upper for pattern in SENSITIVE_ENV_PATTERNS)


def x_is_sensitive_env_var__mutmut_3(name: str) -> bool:
    """Check if environment variable name indicates sensitive data.

    Args:
        name: Environment variable name

    Returns:
        True if the name suggests sensitive data

    """
    name_upper = name.upper()
    return any(None)


def x_is_sensitive_env_var__mutmut_4(name: str) -> bool:
    """Check if environment variable name indicates sensitive data.

    Args:
        name: Environment variable name

    Returns:
        True if the name suggests sensitive data

    """
    name_upper = name.upper()
    return any(pattern not in name_upper for pattern in SENSITIVE_ENV_PATTERNS)

x_is_sensitive_env_var__mutmut_mutants : ClassVar[MutantDict] = {
'x_is_sensitive_env_var__mutmut_1': x_is_sensitive_env_var__mutmut_1, 
    'x_is_sensitive_env_var__mutmut_2': x_is_sensitive_env_var__mutmut_2, 
    'x_is_sensitive_env_var__mutmut_3': x_is_sensitive_env_var__mutmut_3, 
    'x_is_sensitive_env_var__mutmut_4': x_is_sensitive_env_var__mutmut_4
}

def is_sensitive_env_var(*args, **kwargs):
    result = _mutmut_trampoline(x_is_sensitive_env_var__mutmut_orig, x_is_sensitive_env_var__mutmut_mutants, args, kwargs)
    return result 

is_sensitive_env_var.__signature__ = _mutmut_signature(x_is_sensitive_env_var__mutmut_orig)
x_is_sensitive_env_var__mutmut_orig.__name__ = 'x_is_sensitive_env_var'


def x_scrub_environment__mutmut_orig(
    env: Mapping[str, str],
    allowlist: set[str] | None = None,
    enabled: bool = DEFAULT_ENV_SCRUBBING_ENABLED,
) -> dict[str, str]:
    """Scrub environment to only include allowlisted variables.

    This function filters the environment to only include safe, non-sensitive
    variables from a curated allowlist. This prevents credential leakage when
    environment variables are logged or stored.

    Args:
        env: Environment dictionary to scrub
        allowlist: Set of allowed variable names (defaults to SAFE_ENV_ALLOWLIST)
        enabled: Whether scrubbing is enabled (default: True)

    Returns:
        Scrubbed environment dictionary containing only allowlisted variables

    Examples:
        >>> import os
        >>> scrubbed = scrub_environment(os.environ)
        >>> "PATH" in scrubbed  # Safe variable included
        True
        >>> "AWS_SECRET_ACCESS_KEY" in scrubbed  # Secret excluded
        False

    """
    if not enabled:
        return dict(env)

    if allowlist is None:
        allowlist = SAFE_ENV_ALLOWLIST

    # Only include variables in the allowlist
    return {key: value for key, value in env.items() if key in allowlist}


def x_scrub_environment__mutmut_1(
    env: Mapping[str, str],
    allowlist: set[str] | None = None,
    enabled: bool = DEFAULT_ENV_SCRUBBING_ENABLED,
) -> dict[str, str]:
    """Scrub environment to only include allowlisted variables.

    This function filters the environment to only include safe, non-sensitive
    variables from a curated allowlist. This prevents credential leakage when
    environment variables are logged or stored.

    Args:
        env: Environment dictionary to scrub
        allowlist: Set of allowed variable names (defaults to SAFE_ENV_ALLOWLIST)
        enabled: Whether scrubbing is enabled (default: True)

    Returns:
        Scrubbed environment dictionary containing only allowlisted variables

    Examples:
        >>> import os
        >>> scrubbed = scrub_environment(os.environ)
        >>> "PATH" in scrubbed  # Safe variable included
        True
        >>> "AWS_SECRET_ACCESS_KEY" in scrubbed  # Secret excluded
        False

    """
    if enabled:
        return dict(env)

    if allowlist is None:
        allowlist = SAFE_ENV_ALLOWLIST

    # Only include variables in the allowlist
    return {key: value for key, value in env.items() if key in allowlist}


def x_scrub_environment__mutmut_2(
    env: Mapping[str, str],
    allowlist: set[str] | None = None,
    enabled: bool = DEFAULT_ENV_SCRUBBING_ENABLED,
) -> dict[str, str]:
    """Scrub environment to only include allowlisted variables.

    This function filters the environment to only include safe, non-sensitive
    variables from a curated allowlist. This prevents credential leakage when
    environment variables are logged or stored.

    Args:
        env: Environment dictionary to scrub
        allowlist: Set of allowed variable names (defaults to SAFE_ENV_ALLOWLIST)
        enabled: Whether scrubbing is enabled (default: True)

    Returns:
        Scrubbed environment dictionary containing only allowlisted variables

    Examples:
        >>> import os
        >>> scrubbed = scrub_environment(os.environ)
        >>> "PATH" in scrubbed  # Safe variable included
        True
        >>> "AWS_SECRET_ACCESS_KEY" in scrubbed  # Secret excluded
        False

    """
    if not enabled:
        return dict(None)

    if allowlist is None:
        allowlist = SAFE_ENV_ALLOWLIST

    # Only include variables in the allowlist
    return {key: value for key, value in env.items() if key in allowlist}


def x_scrub_environment__mutmut_3(
    env: Mapping[str, str],
    allowlist: set[str] | None = None,
    enabled: bool = DEFAULT_ENV_SCRUBBING_ENABLED,
) -> dict[str, str]:
    """Scrub environment to only include allowlisted variables.

    This function filters the environment to only include safe, non-sensitive
    variables from a curated allowlist. This prevents credential leakage when
    environment variables are logged or stored.

    Args:
        env: Environment dictionary to scrub
        allowlist: Set of allowed variable names (defaults to SAFE_ENV_ALLOWLIST)
        enabled: Whether scrubbing is enabled (default: True)

    Returns:
        Scrubbed environment dictionary containing only allowlisted variables

    Examples:
        >>> import os
        >>> scrubbed = scrub_environment(os.environ)
        >>> "PATH" in scrubbed  # Safe variable included
        True
        >>> "AWS_SECRET_ACCESS_KEY" in scrubbed  # Secret excluded
        False

    """
    if not enabled:
        return dict(env)

    if allowlist is not None:
        allowlist = SAFE_ENV_ALLOWLIST

    # Only include variables in the allowlist
    return {key: value for key, value in env.items() if key in allowlist}


def x_scrub_environment__mutmut_4(
    env: Mapping[str, str],
    allowlist: set[str] | None = None,
    enabled: bool = DEFAULT_ENV_SCRUBBING_ENABLED,
) -> dict[str, str]:
    """Scrub environment to only include allowlisted variables.

    This function filters the environment to only include safe, non-sensitive
    variables from a curated allowlist. This prevents credential leakage when
    environment variables are logged or stored.

    Args:
        env: Environment dictionary to scrub
        allowlist: Set of allowed variable names (defaults to SAFE_ENV_ALLOWLIST)
        enabled: Whether scrubbing is enabled (default: True)

    Returns:
        Scrubbed environment dictionary containing only allowlisted variables

    Examples:
        >>> import os
        >>> scrubbed = scrub_environment(os.environ)
        >>> "PATH" in scrubbed  # Safe variable included
        True
        >>> "AWS_SECRET_ACCESS_KEY" in scrubbed  # Secret excluded
        False

    """
    if not enabled:
        return dict(env)

    if allowlist is None:
        allowlist = None

    # Only include variables in the allowlist
    return {key: value for key, value in env.items() if key in allowlist}


def x_scrub_environment__mutmut_5(
    env: Mapping[str, str],
    allowlist: set[str] | None = None,
    enabled: bool = DEFAULT_ENV_SCRUBBING_ENABLED,
) -> dict[str, str]:
    """Scrub environment to only include allowlisted variables.

    This function filters the environment to only include safe, non-sensitive
    variables from a curated allowlist. This prevents credential leakage when
    environment variables are logged or stored.

    Args:
        env: Environment dictionary to scrub
        allowlist: Set of allowed variable names (defaults to SAFE_ENV_ALLOWLIST)
        enabled: Whether scrubbing is enabled (default: True)

    Returns:
        Scrubbed environment dictionary containing only allowlisted variables

    Examples:
        >>> import os
        >>> scrubbed = scrub_environment(os.environ)
        >>> "PATH" in scrubbed  # Safe variable included
        True
        >>> "AWS_SECRET_ACCESS_KEY" in scrubbed  # Secret excluded
        False

    """
    if not enabled:
        return dict(env)

    if allowlist is None:
        allowlist = SAFE_ENV_ALLOWLIST

    # Only include variables in the allowlist
    return {key: value for key, value in env.items() if key not in allowlist}

x_scrub_environment__mutmut_mutants : ClassVar[MutantDict] = {
'x_scrub_environment__mutmut_1': x_scrub_environment__mutmut_1, 
    'x_scrub_environment__mutmut_2': x_scrub_environment__mutmut_2, 
    'x_scrub_environment__mutmut_3': x_scrub_environment__mutmut_3, 
    'x_scrub_environment__mutmut_4': x_scrub_environment__mutmut_4, 
    'x_scrub_environment__mutmut_5': x_scrub_environment__mutmut_5
}

def scrub_environment(*args, **kwargs):
    result = _mutmut_trampoline(x_scrub_environment__mutmut_orig, x_scrub_environment__mutmut_mutants, args, kwargs)
    return result 

scrub_environment.__signature__ = _mutmut_signature(x_scrub_environment__mutmut_orig)
x_scrub_environment__mutmut_orig.__name__ = 'x_scrub_environment'


def x_mask_sensitive_env_vars__mutmut_orig(env: Mapping[str, str]) -> dict[str, str]:
    """Mask sensitive environment variables for safe logging.

    This function creates a copy of the environment with sensitive values
    replaced by "[MASKED]" for safe display in logs.

    Args:
        env: Environment dictionary to mask

    Returns:
        Environment dictionary with sensitive values masked

    Examples:
        >>> env = {"PATH": "/usr/bin", "AWS_SECRET_KEY": "secret123"}
        >>> masked = mask_sensitive_env_vars(env)
        >>> masked["PATH"]
        '/usr/bin'
        >>> masked["AWS_SECRET_KEY"]
        '[MASKED]'

    """
    masked = {}
    for key, value in env.items():
        if is_sensitive_env_var(key):
            masked[key] = "[MASKED]"
        else:
            masked[key] = value
    return masked


def x_mask_sensitive_env_vars__mutmut_1(env: Mapping[str, str]) -> dict[str, str]:
    """Mask sensitive environment variables for safe logging.

    This function creates a copy of the environment with sensitive values
    replaced by "[MASKED]" for safe display in logs.

    Args:
        env: Environment dictionary to mask

    Returns:
        Environment dictionary with sensitive values masked

    Examples:
        >>> env = {"PATH": "/usr/bin", "AWS_SECRET_KEY": "secret123"}
        >>> masked = mask_sensitive_env_vars(env)
        >>> masked["PATH"]
        '/usr/bin'
        >>> masked["AWS_SECRET_KEY"]
        '[MASKED]'

    """
    masked = None
    for key, value in env.items():
        if is_sensitive_env_var(key):
            masked[key] = "[MASKED]"
        else:
            masked[key] = value
    return masked


def x_mask_sensitive_env_vars__mutmut_2(env: Mapping[str, str]) -> dict[str, str]:
    """Mask sensitive environment variables for safe logging.

    This function creates a copy of the environment with sensitive values
    replaced by "[MASKED]" for safe display in logs.

    Args:
        env: Environment dictionary to mask

    Returns:
        Environment dictionary with sensitive values masked

    Examples:
        >>> env = {"PATH": "/usr/bin", "AWS_SECRET_KEY": "secret123"}
        >>> masked = mask_sensitive_env_vars(env)
        >>> masked["PATH"]
        '/usr/bin'
        >>> masked["AWS_SECRET_KEY"]
        '[MASKED]'

    """
    masked = {}
    for key, value in env.items():
        if is_sensitive_env_var(None):
            masked[key] = "[MASKED]"
        else:
            masked[key] = value
    return masked


def x_mask_sensitive_env_vars__mutmut_3(env: Mapping[str, str]) -> dict[str, str]:
    """Mask sensitive environment variables for safe logging.

    This function creates a copy of the environment with sensitive values
    replaced by "[MASKED]" for safe display in logs.

    Args:
        env: Environment dictionary to mask

    Returns:
        Environment dictionary with sensitive values masked

    Examples:
        >>> env = {"PATH": "/usr/bin", "AWS_SECRET_KEY": "secret123"}
        >>> masked = mask_sensitive_env_vars(env)
        >>> masked["PATH"]
        '/usr/bin'
        >>> masked["AWS_SECRET_KEY"]
        '[MASKED]'

    """
    masked = {}
    for key, value in env.items():
        if is_sensitive_env_var(key):
            masked[key] = None
        else:
            masked[key] = value
    return masked


def x_mask_sensitive_env_vars__mutmut_4(env: Mapping[str, str]) -> dict[str, str]:
    """Mask sensitive environment variables for safe logging.

    This function creates a copy of the environment with sensitive values
    replaced by "[MASKED]" for safe display in logs.

    Args:
        env: Environment dictionary to mask

    Returns:
        Environment dictionary with sensitive values masked

    Examples:
        >>> env = {"PATH": "/usr/bin", "AWS_SECRET_KEY": "secret123"}
        >>> masked = mask_sensitive_env_vars(env)
        >>> masked["PATH"]
        '/usr/bin'
        >>> masked["AWS_SECRET_KEY"]
        '[MASKED]'

    """
    masked = {}
    for key, value in env.items():
        if is_sensitive_env_var(key):
            masked[key] = "XX[MASKED]XX"
        else:
            masked[key] = value
    return masked


def x_mask_sensitive_env_vars__mutmut_5(env: Mapping[str, str]) -> dict[str, str]:
    """Mask sensitive environment variables for safe logging.

    This function creates a copy of the environment with sensitive values
    replaced by "[MASKED]" for safe display in logs.

    Args:
        env: Environment dictionary to mask

    Returns:
        Environment dictionary with sensitive values masked

    Examples:
        >>> env = {"PATH": "/usr/bin", "AWS_SECRET_KEY": "secret123"}
        >>> masked = mask_sensitive_env_vars(env)
        >>> masked["PATH"]
        '/usr/bin'
        >>> masked["AWS_SECRET_KEY"]
        '[MASKED]'

    """
    masked = {}
    for key, value in env.items():
        if is_sensitive_env_var(key):
            masked[key] = "[masked]"
        else:
            masked[key] = value
    return masked


def x_mask_sensitive_env_vars__mutmut_6(env: Mapping[str, str]) -> dict[str, str]:
    """Mask sensitive environment variables for safe logging.

    This function creates a copy of the environment with sensitive values
    replaced by "[MASKED]" for safe display in logs.

    Args:
        env: Environment dictionary to mask

    Returns:
        Environment dictionary with sensitive values masked

    Examples:
        >>> env = {"PATH": "/usr/bin", "AWS_SECRET_KEY": "secret123"}
        >>> masked = mask_sensitive_env_vars(env)
        >>> masked["PATH"]
        '/usr/bin'
        >>> masked["AWS_SECRET_KEY"]
        '[MASKED]'

    """
    masked = {}
    for key, value in env.items():
        if is_sensitive_env_var(key):
            masked[key] = "[MASKED]"
        else:
            masked[key] = None
    return masked

x_mask_sensitive_env_vars__mutmut_mutants : ClassVar[MutantDict] = {
'x_mask_sensitive_env_vars__mutmut_1': x_mask_sensitive_env_vars__mutmut_1, 
    'x_mask_sensitive_env_vars__mutmut_2': x_mask_sensitive_env_vars__mutmut_2, 
    'x_mask_sensitive_env_vars__mutmut_3': x_mask_sensitive_env_vars__mutmut_3, 
    'x_mask_sensitive_env_vars__mutmut_4': x_mask_sensitive_env_vars__mutmut_4, 
    'x_mask_sensitive_env_vars__mutmut_5': x_mask_sensitive_env_vars__mutmut_5, 
    'x_mask_sensitive_env_vars__mutmut_6': x_mask_sensitive_env_vars__mutmut_6
}

def mask_sensitive_env_vars(*args, **kwargs):
    result = _mutmut_trampoline(x_mask_sensitive_env_vars__mutmut_orig, x_mask_sensitive_env_vars__mutmut_mutants, args, kwargs)
    return result 

mask_sensitive_env_vars.__signature__ = _mutmut_signature(x_mask_sensitive_env_vars__mutmut_orig)
x_mask_sensitive_env_vars__mutmut_orig.__name__ = 'x_mask_sensitive_env_vars'


def x_prepare_subprocess_environment__mutmut_orig(
    caller_overrides: Mapping[str, str] | None = None,
    scrub: bool = DEFAULT_ENV_SCRUBBING_ENABLED,
    allowlist: set[str] | None = None,
) -> dict[str, str]:
    """Prepare environment for subprocess execution with scrubbing.

    This function creates a minimal, safe environment for subprocess execution
    by combining allowlisted system variables with caller-provided overrides.

    Args:
        caller_overrides: Environment variables provided by caller (always included)
        scrub: Whether to scrub the base environment (default: True)
        allowlist: Custom allowlist (defaults to SAFE_ENV_ALLOWLIST)

    Returns:
        Environment dictionary for subprocess

    Security Note:
        - If scrub=True: Only allowlisted system vars + caller overrides included
        - If scrub=False: Full os.environ + caller overrides (NOT RECOMMENDED)
        - Caller overrides always included (caller is trusted)
        - PROVIDE_TELEMETRY_DISABLED always added to prevent recursive logging

    """
    # Start with either scrubbed or full environment
    run_env = (
        scrub_environment(os.environ, allowlist=allowlist, enabled=True)
        if scrub
        else os.environ.copy()  # Not recommended - use scrub=True
    )

    # Merge caller-provided overrides (always trusted)
    if caller_overrides is not None:
        run_env.update(caller_overrides)

    # Always disable telemetry in subprocesses to avoid recursive logging
    run_env.setdefault("PROVIDE_TELEMETRY_DISABLED", "true")

    return run_env


def x_prepare_subprocess_environment__mutmut_1(
    caller_overrides: Mapping[str, str] | None = None,
    scrub: bool = DEFAULT_ENV_SCRUBBING_ENABLED,
    allowlist: set[str] | None = None,
) -> dict[str, str]:
    """Prepare environment for subprocess execution with scrubbing.

    This function creates a minimal, safe environment for subprocess execution
    by combining allowlisted system variables with caller-provided overrides.

    Args:
        caller_overrides: Environment variables provided by caller (always included)
        scrub: Whether to scrub the base environment (default: True)
        allowlist: Custom allowlist (defaults to SAFE_ENV_ALLOWLIST)

    Returns:
        Environment dictionary for subprocess

    Security Note:
        - If scrub=True: Only allowlisted system vars + caller overrides included
        - If scrub=False: Full os.environ + caller overrides (NOT RECOMMENDED)
        - Caller overrides always included (caller is trusted)
        - PROVIDE_TELEMETRY_DISABLED always added to prevent recursive logging

    """
    # Start with either scrubbed or full environment
    run_env = None

    # Merge caller-provided overrides (always trusted)
    if caller_overrides is not None:
        run_env.update(caller_overrides)

    # Always disable telemetry in subprocesses to avoid recursive logging
    run_env.setdefault("PROVIDE_TELEMETRY_DISABLED", "true")

    return run_env


def x_prepare_subprocess_environment__mutmut_2(
    caller_overrides: Mapping[str, str] | None = None,
    scrub: bool = DEFAULT_ENV_SCRUBBING_ENABLED,
    allowlist: set[str] | None = None,
) -> dict[str, str]:
    """Prepare environment for subprocess execution with scrubbing.

    This function creates a minimal, safe environment for subprocess execution
    by combining allowlisted system variables with caller-provided overrides.

    Args:
        caller_overrides: Environment variables provided by caller (always included)
        scrub: Whether to scrub the base environment (default: True)
        allowlist: Custom allowlist (defaults to SAFE_ENV_ALLOWLIST)

    Returns:
        Environment dictionary for subprocess

    Security Note:
        - If scrub=True: Only allowlisted system vars + caller overrides included
        - If scrub=False: Full os.environ + caller overrides (NOT RECOMMENDED)
        - Caller overrides always included (caller is trusted)
        - PROVIDE_TELEMETRY_DISABLED always added to prevent recursive logging

    """
    # Start with either scrubbed or full environment
    run_env = (
        scrub_environment(None, allowlist=allowlist, enabled=True)
        if scrub
        else os.environ.copy()  # Not recommended - use scrub=True
    )

    # Merge caller-provided overrides (always trusted)
    if caller_overrides is not None:
        run_env.update(caller_overrides)

    # Always disable telemetry in subprocesses to avoid recursive logging
    run_env.setdefault("PROVIDE_TELEMETRY_DISABLED", "true")

    return run_env


def x_prepare_subprocess_environment__mutmut_3(
    caller_overrides: Mapping[str, str] | None = None,
    scrub: bool = DEFAULT_ENV_SCRUBBING_ENABLED,
    allowlist: set[str] | None = None,
) -> dict[str, str]:
    """Prepare environment for subprocess execution with scrubbing.

    This function creates a minimal, safe environment for subprocess execution
    by combining allowlisted system variables with caller-provided overrides.

    Args:
        caller_overrides: Environment variables provided by caller (always included)
        scrub: Whether to scrub the base environment (default: True)
        allowlist: Custom allowlist (defaults to SAFE_ENV_ALLOWLIST)

    Returns:
        Environment dictionary for subprocess

    Security Note:
        - If scrub=True: Only allowlisted system vars + caller overrides included
        - If scrub=False: Full os.environ + caller overrides (NOT RECOMMENDED)
        - Caller overrides always included (caller is trusted)
        - PROVIDE_TELEMETRY_DISABLED always added to prevent recursive logging

    """
    # Start with either scrubbed or full environment
    run_env = (
        scrub_environment(os.environ, allowlist=None, enabled=True)
        if scrub
        else os.environ.copy()  # Not recommended - use scrub=True
    )

    # Merge caller-provided overrides (always trusted)
    if caller_overrides is not None:
        run_env.update(caller_overrides)

    # Always disable telemetry in subprocesses to avoid recursive logging
    run_env.setdefault("PROVIDE_TELEMETRY_DISABLED", "true")

    return run_env


def x_prepare_subprocess_environment__mutmut_4(
    caller_overrides: Mapping[str, str] | None = None,
    scrub: bool = DEFAULT_ENV_SCRUBBING_ENABLED,
    allowlist: set[str] | None = None,
) -> dict[str, str]:
    """Prepare environment for subprocess execution with scrubbing.

    This function creates a minimal, safe environment for subprocess execution
    by combining allowlisted system variables with caller-provided overrides.

    Args:
        caller_overrides: Environment variables provided by caller (always included)
        scrub: Whether to scrub the base environment (default: True)
        allowlist: Custom allowlist (defaults to SAFE_ENV_ALLOWLIST)

    Returns:
        Environment dictionary for subprocess

    Security Note:
        - If scrub=True: Only allowlisted system vars + caller overrides included
        - If scrub=False: Full os.environ + caller overrides (NOT RECOMMENDED)
        - Caller overrides always included (caller is trusted)
        - PROVIDE_TELEMETRY_DISABLED always added to prevent recursive logging

    """
    # Start with either scrubbed or full environment
    run_env = (
        scrub_environment(os.environ, allowlist=allowlist, enabled=None)
        if scrub
        else os.environ.copy()  # Not recommended - use scrub=True
    )

    # Merge caller-provided overrides (always trusted)
    if caller_overrides is not None:
        run_env.update(caller_overrides)

    # Always disable telemetry in subprocesses to avoid recursive logging
    run_env.setdefault("PROVIDE_TELEMETRY_DISABLED", "true")

    return run_env


def x_prepare_subprocess_environment__mutmut_5(
    caller_overrides: Mapping[str, str] | None = None,
    scrub: bool = DEFAULT_ENV_SCRUBBING_ENABLED,
    allowlist: set[str] | None = None,
) -> dict[str, str]:
    """Prepare environment for subprocess execution with scrubbing.

    This function creates a minimal, safe environment for subprocess execution
    by combining allowlisted system variables with caller-provided overrides.

    Args:
        caller_overrides: Environment variables provided by caller (always included)
        scrub: Whether to scrub the base environment (default: True)
        allowlist: Custom allowlist (defaults to SAFE_ENV_ALLOWLIST)

    Returns:
        Environment dictionary for subprocess

    Security Note:
        - If scrub=True: Only allowlisted system vars + caller overrides included
        - If scrub=False: Full os.environ + caller overrides (NOT RECOMMENDED)
        - Caller overrides always included (caller is trusted)
        - PROVIDE_TELEMETRY_DISABLED always added to prevent recursive logging

    """
    # Start with either scrubbed or full environment
    run_env = (
        scrub_environment(allowlist=allowlist, enabled=True)
        if scrub
        else os.environ.copy()  # Not recommended - use scrub=True
    )

    # Merge caller-provided overrides (always trusted)
    if caller_overrides is not None:
        run_env.update(caller_overrides)

    # Always disable telemetry in subprocesses to avoid recursive logging
    run_env.setdefault("PROVIDE_TELEMETRY_DISABLED", "true")

    return run_env


def x_prepare_subprocess_environment__mutmut_6(
    caller_overrides: Mapping[str, str] | None = None,
    scrub: bool = DEFAULT_ENV_SCRUBBING_ENABLED,
    allowlist: set[str] | None = None,
) -> dict[str, str]:
    """Prepare environment for subprocess execution with scrubbing.

    This function creates a minimal, safe environment for subprocess execution
    by combining allowlisted system variables with caller-provided overrides.

    Args:
        caller_overrides: Environment variables provided by caller (always included)
        scrub: Whether to scrub the base environment (default: True)
        allowlist: Custom allowlist (defaults to SAFE_ENV_ALLOWLIST)

    Returns:
        Environment dictionary for subprocess

    Security Note:
        - If scrub=True: Only allowlisted system vars + caller overrides included
        - If scrub=False: Full os.environ + caller overrides (NOT RECOMMENDED)
        - Caller overrides always included (caller is trusted)
        - PROVIDE_TELEMETRY_DISABLED always added to prevent recursive logging

    """
    # Start with either scrubbed or full environment
    run_env = (
        scrub_environment(os.environ, enabled=True)
        if scrub
        else os.environ.copy()  # Not recommended - use scrub=True
    )

    # Merge caller-provided overrides (always trusted)
    if caller_overrides is not None:
        run_env.update(caller_overrides)

    # Always disable telemetry in subprocesses to avoid recursive logging
    run_env.setdefault("PROVIDE_TELEMETRY_DISABLED", "true")

    return run_env


def x_prepare_subprocess_environment__mutmut_7(
    caller_overrides: Mapping[str, str] | None = None,
    scrub: bool = DEFAULT_ENV_SCRUBBING_ENABLED,
    allowlist: set[str] | None = None,
) -> dict[str, str]:
    """Prepare environment for subprocess execution with scrubbing.

    This function creates a minimal, safe environment for subprocess execution
    by combining allowlisted system variables with caller-provided overrides.

    Args:
        caller_overrides: Environment variables provided by caller (always included)
        scrub: Whether to scrub the base environment (default: True)
        allowlist: Custom allowlist (defaults to SAFE_ENV_ALLOWLIST)

    Returns:
        Environment dictionary for subprocess

    Security Note:
        - If scrub=True: Only allowlisted system vars + caller overrides included
        - If scrub=False: Full os.environ + caller overrides (NOT RECOMMENDED)
        - Caller overrides always included (caller is trusted)
        - PROVIDE_TELEMETRY_DISABLED always added to prevent recursive logging

    """
    # Start with either scrubbed or full environment
    run_env = (
        scrub_environment(os.environ, allowlist=allowlist, )
        if scrub
        else os.environ.copy()  # Not recommended - use scrub=True
    )

    # Merge caller-provided overrides (always trusted)
    if caller_overrides is not None:
        run_env.update(caller_overrides)

    # Always disable telemetry in subprocesses to avoid recursive logging
    run_env.setdefault("PROVIDE_TELEMETRY_DISABLED", "true")

    return run_env


def x_prepare_subprocess_environment__mutmut_8(
    caller_overrides: Mapping[str, str] | None = None,
    scrub: bool = DEFAULT_ENV_SCRUBBING_ENABLED,
    allowlist: set[str] | None = None,
) -> dict[str, str]:
    """Prepare environment for subprocess execution with scrubbing.

    This function creates a minimal, safe environment for subprocess execution
    by combining allowlisted system variables with caller-provided overrides.

    Args:
        caller_overrides: Environment variables provided by caller (always included)
        scrub: Whether to scrub the base environment (default: True)
        allowlist: Custom allowlist (defaults to SAFE_ENV_ALLOWLIST)

    Returns:
        Environment dictionary for subprocess

    Security Note:
        - If scrub=True: Only allowlisted system vars + caller overrides included
        - If scrub=False: Full os.environ + caller overrides (NOT RECOMMENDED)
        - Caller overrides always included (caller is trusted)
        - PROVIDE_TELEMETRY_DISABLED always added to prevent recursive logging

    """
    # Start with either scrubbed or full environment
    run_env = (
        scrub_environment(os.environ, allowlist=allowlist, enabled=False)
        if scrub
        else os.environ.copy()  # Not recommended - use scrub=True
    )

    # Merge caller-provided overrides (always trusted)
    if caller_overrides is not None:
        run_env.update(caller_overrides)

    # Always disable telemetry in subprocesses to avoid recursive logging
    run_env.setdefault("PROVIDE_TELEMETRY_DISABLED", "true")

    return run_env


def x_prepare_subprocess_environment__mutmut_9(
    caller_overrides: Mapping[str, str] | None = None,
    scrub: bool = DEFAULT_ENV_SCRUBBING_ENABLED,
    allowlist: set[str] | None = None,
) -> dict[str, str]:
    """Prepare environment for subprocess execution with scrubbing.

    This function creates a minimal, safe environment for subprocess execution
    by combining allowlisted system variables with caller-provided overrides.

    Args:
        caller_overrides: Environment variables provided by caller (always included)
        scrub: Whether to scrub the base environment (default: True)
        allowlist: Custom allowlist (defaults to SAFE_ENV_ALLOWLIST)

    Returns:
        Environment dictionary for subprocess

    Security Note:
        - If scrub=True: Only allowlisted system vars + caller overrides included
        - If scrub=False: Full os.environ + caller overrides (NOT RECOMMENDED)
        - Caller overrides always included (caller is trusted)
        - PROVIDE_TELEMETRY_DISABLED always added to prevent recursive logging

    """
    # Start with either scrubbed or full environment
    run_env = (
        scrub_environment(os.environ, allowlist=allowlist, enabled=True)
        if scrub
        else os.environ.copy()  # Not recommended - use scrub=True
    )

    # Merge caller-provided overrides (always trusted)
    if caller_overrides is None:
        run_env.update(caller_overrides)

    # Always disable telemetry in subprocesses to avoid recursive logging
    run_env.setdefault("PROVIDE_TELEMETRY_DISABLED", "true")

    return run_env


def x_prepare_subprocess_environment__mutmut_10(
    caller_overrides: Mapping[str, str] | None = None,
    scrub: bool = DEFAULT_ENV_SCRUBBING_ENABLED,
    allowlist: set[str] | None = None,
) -> dict[str, str]:
    """Prepare environment for subprocess execution with scrubbing.

    This function creates a minimal, safe environment for subprocess execution
    by combining allowlisted system variables with caller-provided overrides.

    Args:
        caller_overrides: Environment variables provided by caller (always included)
        scrub: Whether to scrub the base environment (default: True)
        allowlist: Custom allowlist (defaults to SAFE_ENV_ALLOWLIST)

    Returns:
        Environment dictionary for subprocess

    Security Note:
        - If scrub=True: Only allowlisted system vars + caller overrides included
        - If scrub=False: Full os.environ + caller overrides (NOT RECOMMENDED)
        - Caller overrides always included (caller is trusted)
        - PROVIDE_TELEMETRY_DISABLED always added to prevent recursive logging

    """
    # Start with either scrubbed or full environment
    run_env = (
        scrub_environment(os.environ, allowlist=allowlist, enabled=True)
        if scrub
        else os.environ.copy()  # Not recommended - use scrub=True
    )

    # Merge caller-provided overrides (always trusted)
    if caller_overrides is not None:
        run_env.update(None)

    # Always disable telemetry in subprocesses to avoid recursive logging
    run_env.setdefault("PROVIDE_TELEMETRY_DISABLED", "true")

    return run_env


def x_prepare_subprocess_environment__mutmut_11(
    caller_overrides: Mapping[str, str] | None = None,
    scrub: bool = DEFAULT_ENV_SCRUBBING_ENABLED,
    allowlist: set[str] | None = None,
) -> dict[str, str]:
    """Prepare environment for subprocess execution with scrubbing.

    This function creates a minimal, safe environment for subprocess execution
    by combining allowlisted system variables with caller-provided overrides.

    Args:
        caller_overrides: Environment variables provided by caller (always included)
        scrub: Whether to scrub the base environment (default: True)
        allowlist: Custom allowlist (defaults to SAFE_ENV_ALLOWLIST)

    Returns:
        Environment dictionary for subprocess

    Security Note:
        - If scrub=True: Only allowlisted system vars + caller overrides included
        - If scrub=False: Full os.environ + caller overrides (NOT RECOMMENDED)
        - Caller overrides always included (caller is trusted)
        - PROVIDE_TELEMETRY_DISABLED always added to prevent recursive logging

    """
    # Start with either scrubbed or full environment
    run_env = (
        scrub_environment(os.environ, allowlist=allowlist, enabled=True)
        if scrub
        else os.environ.copy()  # Not recommended - use scrub=True
    )

    # Merge caller-provided overrides (always trusted)
    if caller_overrides is not None:
        run_env.update(caller_overrides)

    # Always disable telemetry in subprocesses to avoid recursive logging
    run_env.setdefault(None, "true")

    return run_env


def x_prepare_subprocess_environment__mutmut_12(
    caller_overrides: Mapping[str, str] | None = None,
    scrub: bool = DEFAULT_ENV_SCRUBBING_ENABLED,
    allowlist: set[str] | None = None,
) -> dict[str, str]:
    """Prepare environment for subprocess execution with scrubbing.

    This function creates a minimal, safe environment for subprocess execution
    by combining allowlisted system variables with caller-provided overrides.

    Args:
        caller_overrides: Environment variables provided by caller (always included)
        scrub: Whether to scrub the base environment (default: True)
        allowlist: Custom allowlist (defaults to SAFE_ENV_ALLOWLIST)

    Returns:
        Environment dictionary for subprocess

    Security Note:
        - If scrub=True: Only allowlisted system vars + caller overrides included
        - If scrub=False: Full os.environ + caller overrides (NOT RECOMMENDED)
        - Caller overrides always included (caller is trusted)
        - PROVIDE_TELEMETRY_DISABLED always added to prevent recursive logging

    """
    # Start with either scrubbed or full environment
    run_env = (
        scrub_environment(os.environ, allowlist=allowlist, enabled=True)
        if scrub
        else os.environ.copy()  # Not recommended - use scrub=True
    )

    # Merge caller-provided overrides (always trusted)
    if caller_overrides is not None:
        run_env.update(caller_overrides)

    # Always disable telemetry in subprocesses to avoid recursive logging
    run_env.setdefault("PROVIDE_TELEMETRY_DISABLED", None)

    return run_env


def x_prepare_subprocess_environment__mutmut_13(
    caller_overrides: Mapping[str, str] | None = None,
    scrub: bool = DEFAULT_ENV_SCRUBBING_ENABLED,
    allowlist: set[str] | None = None,
) -> dict[str, str]:
    """Prepare environment for subprocess execution with scrubbing.

    This function creates a minimal, safe environment for subprocess execution
    by combining allowlisted system variables with caller-provided overrides.

    Args:
        caller_overrides: Environment variables provided by caller (always included)
        scrub: Whether to scrub the base environment (default: True)
        allowlist: Custom allowlist (defaults to SAFE_ENV_ALLOWLIST)

    Returns:
        Environment dictionary for subprocess

    Security Note:
        - If scrub=True: Only allowlisted system vars + caller overrides included
        - If scrub=False: Full os.environ + caller overrides (NOT RECOMMENDED)
        - Caller overrides always included (caller is trusted)
        - PROVIDE_TELEMETRY_DISABLED always added to prevent recursive logging

    """
    # Start with either scrubbed or full environment
    run_env = (
        scrub_environment(os.environ, allowlist=allowlist, enabled=True)
        if scrub
        else os.environ.copy()  # Not recommended - use scrub=True
    )

    # Merge caller-provided overrides (always trusted)
    if caller_overrides is not None:
        run_env.update(caller_overrides)

    # Always disable telemetry in subprocesses to avoid recursive logging
    run_env.setdefault("true")

    return run_env


def x_prepare_subprocess_environment__mutmut_14(
    caller_overrides: Mapping[str, str] | None = None,
    scrub: bool = DEFAULT_ENV_SCRUBBING_ENABLED,
    allowlist: set[str] | None = None,
) -> dict[str, str]:
    """Prepare environment for subprocess execution with scrubbing.

    This function creates a minimal, safe environment for subprocess execution
    by combining allowlisted system variables with caller-provided overrides.

    Args:
        caller_overrides: Environment variables provided by caller (always included)
        scrub: Whether to scrub the base environment (default: True)
        allowlist: Custom allowlist (defaults to SAFE_ENV_ALLOWLIST)

    Returns:
        Environment dictionary for subprocess

    Security Note:
        - If scrub=True: Only allowlisted system vars + caller overrides included
        - If scrub=False: Full os.environ + caller overrides (NOT RECOMMENDED)
        - Caller overrides always included (caller is trusted)
        - PROVIDE_TELEMETRY_DISABLED always added to prevent recursive logging

    """
    # Start with either scrubbed or full environment
    run_env = (
        scrub_environment(os.environ, allowlist=allowlist, enabled=True)
        if scrub
        else os.environ.copy()  # Not recommended - use scrub=True
    )

    # Merge caller-provided overrides (always trusted)
    if caller_overrides is not None:
        run_env.update(caller_overrides)

    # Always disable telemetry in subprocesses to avoid recursive logging
    run_env.setdefault("PROVIDE_TELEMETRY_DISABLED", )

    return run_env


def x_prepare_subprocess_environment__mutmut_15(
    caller_overrides: Mapping[str, str] | None = None,
    scrub: bool = DEFAULT_ENV_SCRUBBING_ENABLED,
    allowlist: set[str] | None = None,
) -> dict[str, str]:
    """Prepare environment for subprocess execution with scrubbing.

    This function creates a minimal, safe environment for subprocess execution
    by combining allowlisted system variables with caller-provided overrides.

    Args:
        caller_overrides: Environment variables provided by caller (always included)
        scrub: Whether to scrub the base environment (default: True)
        allowlist: Custom allowlist (defaults to SAFE_ENV_ALLOWLIST)

    Returns:
        Environment dictionary for subprocess

    Security Note:
        - If scrub=True: Only allowlisted system vars + caller overrides included
        - If scrub=False: Full os.environ + caller overrides (NOT RECOMMENDED)
        - Caller overrides always included (caller is trusted)
        - PROVIDE_TELEMETRY_DISABLED always added to prevent recursive logging

    """
    # Start with either scrubbed or full environment
    run_env = (
        scrub_environment(os.environ, allowlist=allowlist, enabled=True)
        if scrub
        else os.environ.copy()  # Not recommended - use scrub=True
    )

    # Merge caller-provided overrides (always trusted)
    if caller_overrides is not None:
        run_env.update(caller_overrides)

    # Always disable telemetry in subprocesses to avoid recursive logging
    run_env.setdefault("XXPROVIDE_TELEMETRY_DISABLEDXX", "true")

    return run_env


def x_prepare_subprocess_environment__mutmut_16(
    caller_overrides: Mapping[str, str] | None = None,
    scrub: bool = DEFAULT_ENV_SCRUBBING_ENABLED,
    allowlist: set[str] | None = None,
) -> dict[str, str]:
    """Prepare environment for subprocess execution with scrubbing.

    This function creates a minimal, safe environment for subprocess execution
    by combining allowlisted system variables with caller-provided overrides.

    Args:
        caller_overrides: Environment variables provided by caller (always included)
        scrub: Whether to scrub the base environment (default: True)
        allowlist: Custom allowlist (defaults to SAFE_ENV_ALLOWLIST)

    Returns:
        Environment dictionary for subprocess

    Security Note:
        - If scrub=True: Only allowlisted system vars + caller overrides included
        - If scrub=False: Full os.environ + caller overrides (NOT RECOMMENDED)
        - Caller overrides always included (caller is trusted)
        - PROVIDE_TELEMETRY_DISABLED always added to prevent recursive logging

    """
    # Start with either scrubbed or full environment
    run_env = (
        scrub_environment(os.environ, allowlist=allowlist, enabled=True)
        if scrub
        else os.environ.copy()  # Not recommended - use scrub=True
    )

    # Merge caller-provided overrides (always trusted)
    if caller_overrides is not None:
        run_env.update(caller_overrides)

    # Always disable telemetry in subprocesses to avoid recursive logging
    run_env.setdefault("provide_telemetry_disabled", "true")

    return run_env


def x_prepare_subprocess_environment__mutmut_17(
    caller_overrides: Mapping[str, str] | None = None,
    scrub: bool = DEFAULT_ENV_SCRUBBING_ENABLED,
    allowlist: set[str] | None = None,
) -> dict[str, str]:
    """Prepare environment for subprocess execution with scrubbing.

    This function creates a minimal, safe environment for subprocess execution
    by combining allowlisted system variables with caller-provided overrides.

    Args:
        caller_overrides: Environment variables provided by caller (always included)
        scrub: Whether to scrub the base environment (default: True)
        allowlist: Custom allowlist (defaults to SAFE_ENV_ALLOWLIST)

    Returns:
        Environment dictionary for subprocess

    Security Note:
        - If scrub=True: Only allowlisted system vars + caller overrides included
        - If scrub=False: Full os.environ + caller overrides (NOT RECOMMENDED)
        - Caller overrides always included (caller is trusted)
        - PROVIDE_TELEMETRY_DISABLED always added to prevent recursive logging

    """
    # Start with either scrubbed or full environment
    run_env = (
        scrub_environment(os.environ, allowlist=allowlist, enabled=True)
        if scrub
        else os.environ.copy()  # Not recommended - use scrub=True
    )

    # Merge caller-provided overrides (always trusted)
    if caller_overrides is not None:
        run_env.update(caller_overrides)

    # Always disable telemetry in subprocesses to avoid recursive logging
    run_env.setdefault("PROVIDE_TELEMETRY_DISABLED", "XXtrueXX")

    return run_env


def x_prepare_subprocess_environment__mutmut_18(
    caller_overrides: Mapping[str, str] | None = None,
    scrub: bool = DEFAULT_ENV_SCRUBBING_ENABLED,
    allowlist: set[str] | None = None,
) -> dict[str, str]:
    """Prepare environment for subprocess execution with scrubbing.

    This function creates a minimal, safe environment for subprocess execution
    by combining allowlisted system variables with caller-provided overrides.

    Args:
        caller_overrides: Environment variables provided by caller (always included)
        scrub: Whether to scrub the base environment (default: True)
        allowlist: Custom allowlist (defaults to SAFE_ENV_ALLOWLIST)

    Returns:
        Environment dictionary for subprocess

    Security Note:
        - If scrub=True: Only allowlisted system vars + caller overrides included
        - If scrub=False: Full os.environ + caller overrides (NOT RECOMMENDED)
        - Caller overrides always included (caller is trusted)
        - PROVIDE_TELEMETRY_DISABLED always added to prevent recursive logging

    """
    # Start with either scrubbed or full environment
    run_env = (
        scrub_environment(os.environ, allowlist=allowlist, enabled=True)
        if scrub
        else os.environ.copy()  # Not recommended - use scrub=True
    )

    # Merge caller-provided overrides (always trusted)
    if caller_overrides is not None:
        run_env.update(caller_overrides)

    # Always disable telemetry in subprocesses to avoid recursive logging
    run_env.setdefault("PROVIDE_TELEMETRY_DISABLED", "TRUE")

    return run_env

x_prepare_subprocess_environment__mutmut_mutants : ClassVar[MutantDict] = {
'x_prepare_subprocess_environment__mutmut_1': x_prepare_subprocess_environment__mutmut_1, 
    'x_prepare_subprocess_environment__mutmut_2': x_prepare_subprocess_environment__mutmut_2, 
    'x_prepare_subprocess_environment__mutmut_3': x_prepare_subprocess_environment__mutmut_3, 
    'x_prepare_subprocess_environment__mutmut_4': x_prepare_subprocess_environment__mutmut_4, 
    'x_prepare_subprocess_environment__mutmut_5': x_prepare_subprocess_environment__mutmut_5, 
    'x_prepare_subprocess_environment__mutmut_6': x_prepare_subprocess_environment__mutmut_6, 
    'x_prepare_subprocess_environment__mutmut_7': x_prepare_subprocess_environment__mutmut_7, 
    'x_prepare_subprocess_environment__mutmut_8': x_prepare_subprocess_environment__mutmut_8, 
    'x_prepare_subprocess_environment__mutmut_9': x_prepare_subprocess_environment__mutmut_9, 
    'x_prepare_subprocess_environment__mutmut_10': x_prepare_subprocess_environment__mutmut_10, 
    'x_prepare_subprocess_environment__mutmut_11': x_prepare_subprocess_environment__mutmut_11, 
    'x_prepare_subprocess_environment__mutmut_12': x_prepare_subprocess_environment__mutmut_12, 
    'x_prepare_subprocess_environment__mutmut_13': x_prepare_subprocess_environment__mutmut_13, 
    'x_prepare_subprocess_environment__mutmut_14': x_prepare_subprocess_environment__mutmut_14, 
    'x_prepare_subprocess_environment__mutmut_15': x_prepare_subprocess_environment__mutmut_15, 
    'x_prepare_subprocess_environment__mutmut_16': x_prepare_subprocess_environment__mutmut_16, 
    'x_prepare_subprocess_environment__mutmut_17': x_prepare_subprocess_environment__mutmut_17, 
    'x_prepare_subprocess_environment__mutmut_18': x_prepare_subprocess_environment__mutmut_18
}

def prepare_subprocess_environment(*args, **kwargs):
    result = _mutmut_trampoline(x_prepare_subprocess_environment__mutmut_orig, x_prepare_subprocess_environment__mutmut_mutants, args, kwargs)
    return result 

prepare_subprocess_environment.__signature__ = _mutmut_signature(x_prepare_subprocess_environment__mutmut_orig)
x_prepare_subprocess_environment__mutmut_orig.__name__ = 'x_prepare_subprocess_environment'


__all__ = [
    "SAFE_ENV_ALLOWLIST",
    "SENSITIVE_ENV_PATTERNS",
    "is_sensitive_env_var",
    "mask_sensitive_env_vars",
    "prepare_subprocess_environment",
    "scrub_environment",
]


# <3 🧱🤝🏃🪄
