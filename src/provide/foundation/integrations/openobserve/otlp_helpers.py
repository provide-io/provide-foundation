#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any

"""Helper functions for OTLP integration.

This module contains helper functions extracted from otlp.py to keep
file sizes manageable and improve code organization.
"""


def configure_otlp_exporter(config: Any, oo_config: Any) -> tuple[str, dict[str, str]]:
    """Configure OTLP exporter endpoint and headers.

    Args:
        config: Telemetry configuration
        oo_config: OpenObserve configuration

    Returns:
        Tuple of (logs_endpoint, headers)
    """
    headers = config.get_otlp_headers_dict()
    if oo_config.org:
        headers["organization"] = oo_config.org
    if oo_config.stream:
        headers["stream-name"] = oo_config.stream

    # Determine endpoint for logs
    if config.otlp_traces_endpoint:
        logs_endpoint = config.otlp_traces_endpoint.replace("/v1/traces", "/v1/logs")
    else:
        logs_endpoint = f"{config.otlp_endpoint}/v1/logs"

    return logs_endpoint, headers


def create_otlp_resource(
    service_name: str,
    service_version: str | None,
    resource_class: Any,
    resource_attrs_class: Any,
) -> Any:
    """Create OTLP resource with service information.

    Args:
        service_name: Service name
        service_version: Optional service version
        resource_class: Resource class from OpenTelemetry
        resource_attrs_class: ResourceAttributes class from OpenTelemetry

    Returns:
        Resource instance
    """
    resource_attrs = {
        resource_attrs_class.SERVICE_NAME: service_name,
    }
    if service_version:
        resource_attrs[resource_attrs_class.SERVICE_VERSION] = service_version

    return resource_class.create(resource_attrs)


def add_trace_attributes(attributes: dict[str, Any], trace_module: Any) -> None:
    """Add trace context to attributes if available.

    Args:
        attributes: Dictionary to update with trace context
        trace_module: OpenTelemetry trace module
    """
    current_span = trace_module.get_current_span()
    if current_span and current_span.is_recording():
        span_context = current_span.get_span_context()
        attributes["trace_id"] = f"{span_context.trace_id:032x}"
        attributes["span_id"] = f"{span_context.span_id:016x}"


def map_level_to_severity(level: str) -> int:
    """Map log level string to OTLP severity number.

    Args:
        level: Log level string (e.g., "INFO", "ERROR")

    Returns:
        OTLP severity number (1-21)
    """
    severity_map = {
        "TRACE": 1,
        "DEBUG": 5,
        "INFO": 9,
        "WARN": 13,
        "WARNING": 13,
        "ERROR": 17,
        "FATAL": 21,
        "CRITICAL": 21,
    }
    return severity_map.get(level.upper(), 9)


def add_trace_context_to_log_entry(log_entry: dict[str, Any]) -> None:
    """Add trace context to log entry if available.

    Tries OpenTelemetry trace context first, then Foundation's tracer context.

    Args:
        log_entry: Log entry dictionary to update with trace context
    """
    # Try OpenTelemetry trace context first
    try:
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            log_entry["trace_id"] = f"{span_context.trace_id:032x}"
            log_entry["span_id"] = f"{span_context.span_id:016x}"
            return
    except ImportError:
        pass

    # Try Foundation's tracer context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        span = get_current_span()
        if span:
            log_entry["trace_id"] = span.trace_id
            log_entry["span_id"] = span.span_id
        elif trace_id := get_current_trace_id():
            log_entry["trace_id"] = trace_id
    except ImportError:
        pass


def build_log_entry(
    message: str,
    level: str,
    service: str | None,
    attributes: dict[str, Any] | None,
    config: Any,
) -> dict[str, Any]:
    """Build the log entry dictionary.

    Args:
        message: Log message
        level: Log level
        service: Service name (optional)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context
    """
    from datetime import datetime

    log_entry = {
        "_timestamp": int(datetime.now().timestamp() * 1_000_000),
        "level": level.upper(),
        "message": message,
        "service": service or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_log_entry(log_entry)
    return log_entry


def build_bulk_url(client: Any) -> str:
    """Build the bulk API URL for the client.

    Args:
        client: OpenObserve client instance

    Returns:
        Bulk API URL
    """
    if f"/api/{client.organization}" in client.url:
        return f"{client.url}/_bulk"
    return f"{client.url}/api/{client.organization}/_bulk"


__all__ = [
    "add_trace_attributes",
    "add_trace_context_to_log_entry",
    "build_bulk_url",
    "build_log_entry",
    "configure_otlp_exporter",
    "create_otlp_resource",
    "map_level_to_severity",
]

# 🧱🏗️🔚
