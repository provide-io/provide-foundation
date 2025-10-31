#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Generic OTLP (OpenTelemetry Protocol) support for Foundation logger.

This package provides generic OpenTelemetry Protocol support that can be used
with any OTLP-compatible backend (OpenObserve, Datadog, Honeycomb, etc.).

Key Components:
- OTLPLogClient: Generic client for sending logs via OTLP
- OTLPCircuitBreaker: Reliability pattern for handling endpoint failures
- Helper functions for resource creation, trace context, severity mapping

Example:
    >>> from provide.foundation.logger.otlp import OTLPLogClient
    >>>
    >>> client = OTLPLogClient(
    ...     endpoint="https://api.example.com/v1/logs",
    ...     headers={"Authorization": "Bearer token"},
    ...     service_name="my-service",
    ... )
    >>>
    >>> client.send_log("Hello from OTLP", level="INFO")"""

from __future__ import annotations

from provide.foundation.logger.otlp.circuit import (
    OTLPCircuitBreaker,
    get_otlp_circuit_breaker,
    reset_otlp_circuit_breaker,
)
from provide.foundation.logger.otlp.client import OTLPLogClient
from provide.foundation.logger.otlp.helpers import (
    add_trace_context_to_attributes,
    build_otlp_endpoint,
    build_otlp_headers,
    extract_trace_context,
    normalize_attributes,
)
from provide.foundation.logger.otlp.resource import (
    build_resource_attributes,
    create_otlp_resource,
)
from provide.foundation.logger.otlp.severity import (
    map_level_to_severity,
    map_severity_to_level,
)

__all__ = [
    "OTLPCircuitBreaker",
    "OTLPLogClient",
    "add_trace_context_to_attributes",
    "build_otlp_endpoint",
    "build_otlp_headers",
    "build_resource_attributes",
    "create_otlp_resource",
    "extract_trace_context",
    "get_otlp_circuit_breaker",
    "map_level_to_severity",
    "map_severity_to_level",
    "normalize_attributes",
    "reset_otlp_circuit_breaker",
]

# 🧱🏗️🔚
