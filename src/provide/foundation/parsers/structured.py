#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import TYPE_CHECKING

"""Complex data structure parsers for structured configuration values.

Handles parsing of structured data like dictionaries with specific formats
(headers, module levels, rate limits) from string configuration values.
"""

if TYPE_CHECKING:
    from provide.foundation.logger.types import LogLevelStr
else:
    LogLevelStr = str


def parse_log_level(value: str) -> LogLevelStr:
    """Import parse_log_level from telemetry module to avoid circular imports."""
    from provide.foundation.parsers.telemetry import parse_log_level as _parse_log_level

    return _parse_log_level(value)


def parse_module_levels(value: str | dict[str, str]) -> dict[str, LogLevelStr]:
    """Parse module-specific log levels from string format.

    **Format Requirements:**
    - String format: "module1:LEVEL,module2:LEVEL" (comma-separated pairs)
    - Dict format: Already parsed dictionary (validated and returned)
    - Log levels must be valid: TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    - Module names are trimmed of whitespace
    - Invalid log levels are silently ignored

    **Examples:**
        >>> parse_module_levels("auth.service:DEBUG,database:ERROR")
        {'auth.service': 'DEBUG', 'database': 'ERROR'}

        >>> parse_module_levels("api:INFO")  # Single module
        {'api': 'INFO'}

        >>> parse_module_levels({"web": "warning"})  # Dict input (case normalized)
        {'web': 'WARNING'}

        >>> parse_module_levels("api:INFO,bad:INVALID,db:ERROR")  # Partial success
        {'api': 'INFO', 'db': 'ERROR'}

    Args:
        value: Comma-separated module:level pairs or pre-parsed dict

    Returns:
        Dictionary mapping module names to validated log level strings.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid log levels are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict, validate and return
    if isinstance(value, dict):
        result = {}
        for module, level in value.items():
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid levels silently
                continue
        return result

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if ":" not in pair:
            # Skip invalid entries silently
            continue

        module, level = pair.split(":", 1)
        module = module.strip()
        level = level.strip()

        if module:
            try:
                result[module] = parse_log_level(level)
            except ValueError:
                # Skip invalid log levels silently
                continue

    return result


def parse_rate_limits(value: str) -> dict[str, tuple[float, float]]:
    """Parse per-logger rate limits from string format.

    **Format Requirements:**
    - Comma-separated triplets: "logger1:rate:capacity,logger2:rate:capacity"
    - Rate and capacity must be valid float numbers
    - Logger names are trimmed of whitespace
    - Empty logger names are ignored
    - Invalid entries are silently skipped to allow partial success

    **Examples:**
        >>> parse_rate_limits("api:10.0:100.0,worker:5.0:50.0")
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

        >>> parse_rate_limits("db:1.5:25.0")  # Single entry
        {'db': (1.5, 25.0)}

        >>> parse_rate_limits("api:10:100,invalid:bad,worker:5:50")  # Partial success
        {'api': (10.0, 100.0), 'worker': (5.0, 50.0)}

    Args:
        value: Comma-separated logger:rate:capacity triplets

    Returns:
        Dictionary mapping logger names to (rate, capacity) tuples.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid entries are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    if not value or not value.strip():
        return {}

    result = {}
    for triplet in value.split(","):
        triplet = triplet.strip()
        if not triplet:
            continue

        parts = triplet.split(":")
        if len(parts) != 3:
            # Skip invalid entries silently
            continue

        logger_name, rate_str, capacity_str = parts
        logger_name = logger_name.strip()

        if not logger_name:
            continue

        try:
            rate = float(rate_str.strip())
            capacity = float(capacity_str.strip())
            result[logger_name] = (rate, capacity)
        except (ValueError, TypeError):
            # Skip invalid numeric values silently
            continue

    return result


def parse_headers(value: str | dict[str, str]) -> dict[str, str]:
    """Parse HTTP headers from string format.

    **Format Requirements:**
    - Comma-separated key=value pairs: "key1=value1,key2=value2"
    - Header names and values are trimmed of whitespace
    - Empty header names are ignored
    - Each pair must contain exactly one '=' separator
    - Invalid pairs are silently skipped

    **Examples:**
        >>> parse_headers("Authorization=Bearer token,Content-Type=application/json")
        {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}

        >>> parse_headers("X-API-Key=secret123")  # Single header
        {'X-API-Key': 'secret123'}

        >>> parse_headers("valid=ok,invalid-no-equals,another=good")  # Partial success
        {'valid': 'ok', 'another': 'good'}

        >>> parse_headers("empty-value=")  # Empty values allowed
        {'empty-value': ''}

    Args:
        value: Comma-separated key=value pairs for HTTP headers, or dict if already parsed

    Returns:
        Dictionary of header name-value pairs.
        Invalid entries are silently ignored.

    Note:
        This parser is lenient by design - invalid header pairs are skipped rather than
        raising errors to allow partial configuration success in production environments.

    """
    # If already a dict (from factory default), return as-is
    if isinstance(value, dict):
        return value

    if not value or not value.strip():
        return {}

    result = {}
    for pair in value.split(","):
        pair = pair.strip()
        if not pair:
            continue

        if "=" not in pair:
            # Skip invalid entries
            continue

        key, val = pair.split("=", 1)
        key = key.strip()
        val = val.strip()

        if key:
            result[key] = val

    return result


__all__ = [
    "parse_headers",
    "parse_module_levels",
    "parse_rate_limits",
]

# 🧱🏗️🔚
