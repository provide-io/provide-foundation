#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Generic OTLP helper functions for trace context, endpoints, and log formatting.

Provides utility functions for working with OTLP/OpenTelemetry including:
- Trace context extraction
- Endpoint URL building
- Header construction
- Attribute normalization"""

from __future__ import annotations

import json
from typing import Any


def extract_trace_context() -> dict[str, str] | None:
    """Extract current trace context from OpenTelemetry.

    Extracts trace context from OpenTelemetry if SDK is available
    and a valid span is recording.

    Returns:
        Dict with 'trace_id' and 'span_id', or None if not available

    Examples:
        >>> context = extract_trace_context()
        >>> # Returns {'trace_id': '...', 'span_id': '...'} or None
    """
    try:
        from opentelemetry import trace

        span = trace.get_current_span()
        if span and span.is_recording():
            span_context = span.get_span_context()
            if span_context.is_valid:
                return {
                    "trace_id": format(span_context.trace_id, "032x"),
                    "span_id": format(span_context.span_id, "016x"),
                }
    except ImportError:
        pass

    return None


def add_trace_context_to_attributes(attributes: dict[str, Any]) -> None:
    """Add trace context to attributes dict (modifies in place).

    Extracts trace context and adds trace_id/span_id to attributes.
    Safe to call even if no trace context is available (no-op).

    Args:
        attributes: Dictionary to add trace context to (modified in place)

    Examples:
        >>> attrs = {"key": "value"}
        >>> add_trace_context_to_attributes(attrs)
        >>> # attrs may now include 'trace_id' and 'span_id' if context available
    """
    trace_context = extract_trace_context()
    if trace_context:
        attributes.update(trace_context)


def build_otlp_endpoint(
    base_endpoint: str,
    signal_type: str = "logs",
) -> str:
    """Build OTLP endpoint URL for specific signal type.

    Constructs the full OTLP endpoint URL for the given signal type.
    Handles trailing slashes and is idempotent (won't double-add paths).

    Args:
        base_endpoint: Base OTLP endpoint (e.g., "https://api.example.com")
        signal_type: "logs", "traces", or "metrics"

    Returns:
        Full endpoint URL (e.g., "https://api.example.com/v1/logs")

    Examples:
        >>> build_otlp_endpoint("https://api.example.com")
        'https://api.example.com/v1/logs'

        >>> build_otlp_endpoint("https://api.example.com/", "traces")
        'https://api.example.com/v1/traces'

        >>> build_otlp_endpoint("https://api.example.com/v1/logs")
        'https://api.example.com/v1/logs'
    """
    # Remove trailing slash
    endpoint = base_endpoint.rstrip("/")

    # Check if already has /v1/{signal} path (idempotent)
    expected_suffix = f"/v1/{signal_type}"
    if endpoint.endswith(expected_suffix):
        return endpoint

    # Build full endpoint
    return f"{endpoint}/v1/{signal_type}"


def build_otlp_headers(
    base_headers: dict[str, str] | None = None,
    auth_token: str | None = None,
) -> dict[str, str]:
    """Build OTLP headers with optional authentication.

    Creates headers dictionary with OTLP-required headers and optional auth.

    Args:
        base_headers: Base headers to include
        auth_token: Optional bearer token for authentication

    Returns:
        Complete headers dict with Content-Type and auth

    Examples:
        >>> build_otlp_headers()
        {'Content-Type': 'application/x-protobuf'}

        >>> build_otlp_headers(auth_token="secret123")
        {'Content-Type': 'application/x-protobuf', 'Authorization': 'Bearer secret123'}

        >>> build_otlp_headers(base_headers={"X-Custom": "value"})
        {'X-Custom': 'value', 'Content-Type': 'application/x-protobuf'}
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OTLP content type
    headers.setdefault("Content-Type", "application/x-protobuf")

    # Add auth token if provided
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    return headers


def normalize_attributes(attributes: dict[str, Any]) -> dict[str, Any]:
    """Normalize attribute values for OTLP compatibility.

    Converts non-serializable types to OTLP-compatible values:
    - Non-serializable types → strings
    - Nested dicts → JSON strings
    - Lists → JSON strings
    - None values → empty strings

    Returns new dict (doesn't modify input).

    Args:
        attributes: Dictionary of attributes to normalize

    Returns:
        New dictionary with normalized values

    Examples:
        >>> normalize_attributes({"key": "value"})
        {'key': 'value'}

        >>> normalize_attributes({"num": 42, "list": [1, 2, 3]})
        {'num': 42, 'list': '[1, 2, 3]'}

        >>> normalize_attributes({"nested": {"a": 1}})
        {'nested': '{"a": 1}'}
    """
    normalized: dict[str, Any] = {}

    for key, value in attributes.items():
        if value is None:
            normalized[key] = ""
        elif isinstance(value, (str, int, float, bool)):
            normalized[key] = value
        elif isinstance(value, (dict, list)):
            try:
                normalized[key] = json.dumps(value)
            except (TypeError, ValueError):
                normalized[key] = str(value)
        else:
            normalized[key] = str(value)

    return normalized


__all__ = [
    "add_trace_context_to_attributes",
    "build_otlp_endpoint",
    "build_otlp_headers",
    "extract_trace_context",
    "normalize_attributes",
]

# 🧱🏗️🔚
