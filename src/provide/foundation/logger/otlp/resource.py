#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""OpenTelemetry Resource creation and service attribute management.

Provides functions for building OTLP Resource instances with standard service
attributes according to the OpenTelemetry specification.

Reference: https://opentelemetry.io/docs/specs/otel/resource/semantic_conventions/"""

from __future__ import annotations

from typing import Any


def build_resource_attributes(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build resource attributes dictionary.

    Creates a dictionary with standard OpenTelemetry resource attributes:
    - service.name (required)
    - service.version (optional)
    - deployment.environment (optional)
    - Any additional custom attributes

    Args:
        service_name: Service name (required)
        service_version: Service version (optional)
        environment: Deployment environment (dev, staging, prod, etc.)
        additional_attrs: Additional custom resource attributes

    Returns:
        Dictionary of resource attributes

    Examples:
        >>> build_resource_attributes("my-service")
        {'service.name': 'my-service'}

        >>> build_resource_attributes(
        ...     "my-service",
        ...     service_version="1.2.3",
        ...     environment="production",
        ... )
        {'service.name': 'my-service', 'service.version': '1.2.3', 'deployment.environment': 'production'}
    """
    attrs: dict[str, Any] = {
        "service.name": service_name,
    }

    if service_version:
        attrs["service.version"] = service_version

    if environment:
        attrs["deployment.environment"] = environment

    if additional_attrs:
        attrs.update(additional_attrs)

    return attrs


def create_otlp_resource(
    service_name: str,
    service_version: str | None = None,
    environment: str | None = None,
    additional_attrs: dict[str, Any] | None = None,
) -> Any | None:
    """Create OpenTelemetry Resource instance.

    Attempts to create an OpenTelemetry SDK Resource with the provided attributes.
    Returns None if the OpenTelemetry SDK is not available (optional dependency).

    Args:
        service_name: Service name (required)
        service_version: Service version (optional)
        environment: Deployment environment (optional)
        additional_attrs: Additional custom resource attributes

    Returns:
        Resource instance if OpenTelemetry SDK available, None otherwise

    Examples:
        >>> resource = create_otlp_resource("my-service", service_version="1.0.0")
        >>> # Returns Resource instance or None if SDK not installed

        >>> resource = create_otlp_resource(
        ...     "my-service",
        ...     environment="production",
        ...     additional_attrs={"team": "platform"},
        ... )
    """
    try:
        from opentelemetry.sdk.resources import Resource
    except ImportError:
        return None

    attrs = build_resource_attributes(
        service_name=service_name,
        service_version=service_version,
        environment=environment,
        additional_attrs=additional_attrs,
    )

    return Resource.create(attrs)


__all__ = [
    "build_resource_attributes",
    "create_otlp_resource",
]

# 🧱🏗️🔚
