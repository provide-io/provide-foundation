"""OpenObserve log sending with automatic OTLP/Bulk API fallback.

Provides a unified send_log() function that automatically tries OTLP first
and falls back to the bulk API if OTLP is unavailable or fails.

For direct OTLP control, use OpenObserveOTLPClient from otlp_adapter module.
"""

from __future__ import annotations

from typing import Any

from provide.foundation.integrations.openobserve.bulk_api import send_log_bulk
from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.otlp_adapter import OpenObserveOTLPClient
from provide.foundation.logger import get_logger

log = get_logger(__name__)


def send_log(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    prefer_otlp: bool = True,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OTLP or bulk API with automatic fallback.

    Tries OTLP first if preferred and available, falls back to OpenObserve bulk API.

    Args:
        message: Log message
        level: Log level (INFO, WARN, ERROR, etc.)
        service_name: Service name (follows OTLP standard)
        attributes: Additional log attributes
        prefer_otlp: Try OTLP first if True (default: True)
        client: OpenObserve client for bulk API (creates new if not provided)

    Returns:
        True if sent successfully via OTLP or bulk API

    Examples:
        >>> # Simple usage (tries OTLP, falls back to bulk)
        >>> send_log("User logged in", level="INFO")
        True

        >>> # With attributes
        >>> send_log("Payment processed", attributes={"amount": 99.99, "user_id": 123})
        True

        >>> # Force bulk API only
        >>> send_log("Direct to bulk", prefer_otlp=False)
        True

    Notes:
        For direct OTLP control (e.g., creating LoggerProvider for structlog),
        import OpenObserveOTLPClient from the otlp_adapter module instead.
    """
    # Try OTLP first if preferred
    if prefer_otlp:
        otlp_client = OpenObserveOTLPClient.from_env()
        if otlp_client and otlp_client.is_available():
            if otlp_client.send_log(message, level, attributes):
                return True

    # Fall back to bulk API
    return send_log_bulk(message, level, service_name, attributes, client)


__all__ = ["send_log"]
