#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

"""Telemetry defaults for Foundation configuration."""

# =================================
# Telemetry Defaults
# =================================
DEFAULT_TELEMETRY_GLOBALLY_DISABLED = False
DEFAULT_TRACING_ENABLED = True
DEFAULT_METRICS_ENABLED = True
DEFAULT_OTLP_PROTOCOL = "http/protobuf"
DEFAULT_TRACE_SAMPLE_RATE = 1.0

# =================================
# Factory Functions
# =================================


def default_otlp_headers() -> dict[str, str]:
    """Factory for OTLP headers dictionary."""
    return {}


__all__ = [
    "DEFAULT_METRICS_ENABLED",
    "DEFAULT_OTLP_PROTOCOL",
    "DEFAULT_TELEMETRY_GLOBALLY_DISABLED",
    "DEFAULT_TRACE_SAMPLE_RATE",
    "DEFAULT_TRACING_ENABLED",
    "default_otlp_headers",
]

# 🧱🏗️🔚
