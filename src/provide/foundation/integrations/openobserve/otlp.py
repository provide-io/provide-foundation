"""OpenObserve OTLP integration.

Provides convenience functions for sending logs to OpenObserve via OTLP or bulk API.
"""

from __future__ import annotations

from typing import Any

from provide.foundation.integrations.openobserve.bulk_api import send_log_bulk
from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.otlp_adapter import OpenObserveOTLPClient
from provide.foundation.logger import get_logger

log = get_logger(__name__)


def send_log_otlp(
    message: str,
    level: str = "INFO",
    service: str | None = None,
    attributes: dict[str, Any] | None = None,
) -> bool:
    """Send log via OTLP (OpenObserve-configured).

    Args:
        message: Log message
        level: Log level
        service: Service name (unused, kept for API compatibility)
        attributes: Additional attributes

    Returns:
        True if sent successfully via OTLP, False otherwise

    Examples:
        >>> send_log_otlp("Hello OpenObserve!", level="INFO")
        True
    """
    client = OpenObserveOTLPClient.from_env()
    if not client or not client.is_available():
        return False

    return client.send_log(message, level, attributes)


def send_log(
    message: str,
    level: str = "INFO",
    service: str | None = None,
    attributes: dict[str, Any] | None = None,
    prefer_otlp: bool = True,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OTLP or bulk API.

    Tries OTLP first if preferred and available, falls back to bulk API.

    Args:
        message: Log message
        level: Log level
        service: Service name
        attributes: Additional attributes
        prefer_otlp: Try OTLP first if True
        client: OpenObserve client for bulk API

    Returns:
        True if sent successfully

    Examples:
        >>> send_log("Hello!", level="INFO")
        True

        >>> send_log("Bulk only", prefer_otlp=False)
        True
    """
    # Try OTLP first if preferred
    if prefer_otlp and send_log_otlp(message, level, service, attributes):
        return True

    # Fall back to bulk API
    return send_log_bulk(message, level, service, attributes, client)


def create_otlp_logger_provider() -> Any | None:
    """Create OTLP logger provider (OpenObserve-configured).

    Returns:
        LoggerProvider if OpenObserve/OTLP is available and configured, None otherwise

    Examples:
        >>> provider = create_otlp_logger_provider()
        >>> if provider:
        ...     # Configure structlog with provider
        ...     pass
    """
    client = OpenObserveOTLPClient.from_env()
    if not client or not client.is_available():
        return None

    return client.create_logger_provider()


__all__ = [
    "create_otlp_logger_provider",
    "send_log",
    "send_log_otlp",
]
