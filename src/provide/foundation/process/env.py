#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

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


def is_sensitive_env_var(name: str) -> bool:
    """Check if environment variable name indicates sensitive data.

    Args:
        name: Environment variable name

    Returns:
        True if the name suggests sensitive data

    """
    name_upper = name.upper()
    return any(pattern in name_upper for pattern in SENSITIVE_ENV_PATTERNS)


def scrub_environment(
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


def mask_sensitive_env_vars(env: Mapping[str, str]) -> dict[str, str]:
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


def prepare_subprocess_environment(
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


__all__ = [
    "SAFE_ENV_ALLOWLIST",
    "SENSITIVE_ENV_PATTERNS",
    "is_sensitive_env_var",
    "mask_sensitive_env_vars",
    "prepare_subprocess_environment",
    "scrub_environment",
]

# 🧱🏗️🔚
