#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any

from provide.foundation.hub import get_component_registry
from provide.foundation.hub.components import ComponentCategory
from provide.foundation.logger import get_logger
from provide.foundation.transport.base import Transport
from provide.foundation.transport.errors import TransportNotFoundError
from provide.foundation.transport.types import TransportType

"""Transport registration and discovery using Foundation Hub."""

log = get_logger(__name__)


def register_transport(
    transport_type: TransportType,
    transport_class: type[Transport],
    schemes: list[str] | None = None,
    **metadata: Any,
) -> None:
    """Register a transport implementation in the Hub.

    Args:
        transport_type: The primary transport type
        transport_class: Transport implementation class
        schemes: List of URI schemes this transport handles
        **metadata: Additional metadata for the transport

    """
    registry = get_component_registry()

    # Default schemes to just the transport type
    if schemes is None:
        schemes = [transport_type.value]

    registry.register(
        name=transport_type.value,
        value=transport_class,
        dimension=ComponentCategory.TRANSPORT.value,
        metadata={
            "transport_type": transport_type,
            "schemes": schemes,
            "class_name": transport_class.__name__,
            **metadata,
        },
        replace=True,  # Allow re-registration
    )

    # Logging removed - transport registration happens frequently during test setup
    # and doesn't provide actionable information


def get_transport_for_scheme(scheme: str) -> type[Transport]:
    """Get transport class for a URI scheme.

    Args:
        scheme: URI scheme (e.g., 'http', 'https', 'ws')

    Returns:
        Transport class that handles the scheme

    Raises:
        TransportNotFoundError: If no transport is registered for the scheme

    """
    registry = get_component_registry()

    # Search through registered transports
    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            schemes = entry.metadata.get("schemes", [])
            if scheme.lower() in schemes:
                log.trace(f"Found transport {entry.value.__name__} for scheme '{scheme}'")
                return entry.value

    raise TransportNotFoundError(
        f"No transport registered for scheme: {scheme}",
        scheme=scheme,
    )


def get_transport(uri: str) -> Transport:
    """Get transport instance for a URI.

    Args:
        uri: Full URI to get transport for

    Returns:
        Transport instance ready to use

    Raises:
        TransportNotFoundError: If no transport supports the URI scheme

    """
    scheme = uri.split("://")[0].lower()
    transport_class = get_transport_for_scheme(scheme)
    return transport_class()


def list_registered_transports() -> dict[str, dict[str, Any]]:
    """List all registered transports.

    Returns:
        Dictionary mapping transport names to their info

    """
    registry = get_component_registry()
    transports = {}

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            transports[entry.name] = {
                "class": entry.value,
                "schemes": entry.metadata.get("schemes", []),
                "transport_type": entry.metadata.get("transport_type"),
                "metadata": entry.metadata,
            }

    return transports


def get_transport_info(scheme_or_name: str) -> dict[str, Any] | None:
    """Get detailed information about a transport.

    Args:
        scheme_or_name: URI scheme or transport name

    Returns:
        Transport information or None if not found

    """
    registry = get_component_registry()

    for entry in registry:
        if entry.dimension == ComponentCategory.TRANSPORT.value:
            # Check if it matches by name
            if entry.name == scheme_or_name:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": entry.metadata.get("schemes", []),
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

            # Check if it matches by scheme
            schemes = entry.metadata.get("schemes", [])
            if scheme_or_name.lower() in schemes:
                return {
                    "name": entry.name,
                    "class": entry.value,
                    "schemes": schemes,
                    "transport_type": entry.metadata.get("transport_type"),
                    "metadata": entry.metadata,
                }

    return None


__all__ = [
    "get_transport",
    "get_transport_for_scheme",
    "get_transport_info",
    "list_registered_transports",
    "register_transport",
]

# 🧱🏗️🔚
