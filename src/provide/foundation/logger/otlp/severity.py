#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""OTLP severity level mapping.

Maps between string log levels and OTLP severity numbers according to
the OpenTelemetry specification.

Reference: https://opentelemetry.io/docs/specs/otel/logs/data-model/#field-severitynumber"""

from __future__ import annotations

# OTLP Severity Number ranges (per OpenTelemetry spec):
# 1-4: TRACE level
# 5-8: DEBUG level
# 9-12: INFO level
# 13-16: WARN level
# 17-20: ERROR level
# 21-24: FATAL level

_LEVEL_TO_SEVERITY: dict[str, int] = {
    "TRACE": 1,  # TRACE (1-4)
    "DEBUG": 5,  # DEBUG (5-8)
    "DEBUG2": 6,
    "DEBUG3": 7,
    "DEBUG4": 8,
    "INFO": 9,  # INFO (9-12)
    "INFO2": 10,
    "INFO3": 11,
    "INFO4": 12,
    "WARN": 13,  # WARN (13-16)
    "WARNING": 13,
    "WARN2": 14,
    "WARN3": 15,
    "WARN4": 16,
    "ERROR": 17,  # ERROR (17-20)
    "ERROR2": 18,
    "ERROR3": 19,
    "ERROR4": 20,
    "FATAL": 21,  # FATAL (21-24)
    "CRITICAL": 21,
    "FATAL2": 22,
    "FATAL3": 23,
    "FATAL4": 24,
}

_SEVERITY_TO_LEVEL: dict[int, str] = {
    1: "TRACE",
    2: "TRACE",
    3: "TRACE",
    4: "TRACE",
    5: "DEBUG",
    6: "DEBUG",
    7: "DEBUG",
    8: "DEBUG",
    9: "INFO",
    10: "INFO",
    11: "INFO",
    12: "INFO",
    13: "WARN",
    14: "WARN",
    15: "WARN",
    16: "WARN",
    17: "ERROR",
    18: "ERROR",
    19: "ERROR",
    20: "ERROR",
    21: "FATAL",
    22: "FATAL",
    23: "FATAL",
    24: "FATAL",
}


def map_level_to_severity(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR", "WARN")

    Returns:
        OTLP severity number (1-24)
        Falls back to 9 (INFO) for unknown levels

    Examples:
        >>> map_level_to_severity("INFO")
        9
        >>> map_level_to_severity("ERROR")
        17
        >>> map_level_to_severity("warning")
        13
        >>> map_level_to_severity("unknown")
        9
    """
    return _LEVEL_TO_SEVERITY.get(level.upper(), 9)


def map_severity_to_level(severity: int) -> str:
    """Map OTLP severity number to log level string.

    Args:
        severity: OTLP severity number (1-24)

    Returns:
        Log level string (TRACE, DEBUG, INFO, WARN, ERROR, FATAL)
        Falls back to "INFO" for unknown severity numbers

    Examples:
        >>> map_severity_to_level(9)
        'INFO'
        >>> map_severity_to_level(17)
        'ERROR'
        >>> map_severity_to_level(100)
        'INFO'
    """
    return _SEVERITY_TO_LEVEL.get(severity, "INFO")


__all__ = [
    "map_level_to_severity",
    "map_severity_to_level",
]

# 🧱🏗️🔚
