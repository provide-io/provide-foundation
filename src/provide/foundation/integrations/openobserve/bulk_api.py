#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""OpenObserve bulk API (non-OTLP fallback).

Provides functions for sending logs via OpenObserve's proprietary bulk ingestion API.
This is used as a fallback when OTLP is unavailable or when the circuit breaker is open."""

from __future__ import annotations

import time
from typing import Any

from provide.foundation.hub import get_hub
from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.config import OpenObserveConfig
from provide.foundation.logger import get_logger
from provide.foundation.logger.config.telemetry import TelemetryConfig
from provide.foundation.logger.otlp.helpers import add_trace_context_to_attributes
from provide.foundation.serialization import json_dumps
from provide.foundation.utils.async_helpers import run_async

log = get_logger(__name__)


def build_log_entry(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
) -> dict[str, Any]:
    """Build the log entry dictionary for bulk API.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (optional, follows OTLP standard)
        attributes: Additional attributes (optional)
        config: Telemetry configuration

    Returns:
        Complete log entry dictionary with trace context

    Examples:
        >>> config = TelemetryConfig(service_name="my-service")
        >>> entry = build_log_entry("Hello", "INFO", None, {"key": "value"}, config)
        >>> entry["message"]
        'Hello'
    """
    log_entry: dict[str, Any] = {
        "_timestamp": int(time.time() * 1_000_000),
        "level": level.upper(),
        "message": message,
        "service": service_name or config.service_name or "foundation",
    }

    if attributes:
        log_entry.update(attributes)

    add_trace_context_to_attributes(log_entry)
    return log_entry


def build_bulk_url(client: OpenObserveClient) -> str:
    """Build the bulk API URL for the client.

    Args:
        client: OpenObserve client instance

    Returns:
        Bulk API URL

    Examples:
        >>> client = OpenObserveClient(
        ...     url="https://api.openobserve.ai",
        ...     username="admin",
        ...     password="secret",
        ...     organization="my-org",
        ... )
        >>> build_bulk_url(client)
        'https://api.openobserve.ai/api/my-org/_bulk'
    """
    if f"/api/{client.organization}" in client.url:
        return f"{client.url}/_bulk"
    return f"{client.url}/api/{client.organization}/_bulk"


def build_bulk_request(
    message: str,
    level: str,
    service_name: str | None,
    attributes: dict[str, Any] | None,
    config: TelemetryConfig,
    stream: str,
) -> str:
    """Build NDJSON bulk request payload.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Log attributes
        config: Telemetry configuration
        stream: OpenObserve stream name

    Returns:
        NDJSON-formatted bulk request payload

    Examples:
        >>> config = TelemetryConfig(service_name="test")
        >>> bulk = build_bulk_request("Hello", "INFO", None, None, config, "logs")
        >>> "\\n" in bulk
        True
    """
    log_entry = build_log_entry(message, level, service_name, attributes, config)
    index_line = json_dumps({"index": {"_index": stream}})
    data_line = json_dumps(log_entry)
    return f"{index_line}\n{data_line}\n"


def send_log_bulk(
    message: str,
    level: str = "INFO",
    service_name: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send log via OpenObserve bulk API (non-OTLP).

    This is OpenObserve's proprietary bulk ingestion API, not OTLP.
    Used as fallback when OTLP is unavailable or circuit is open.

    Args:
        message: Log message
        level: Log level
        service_name: Service name (follows OTLP standard)
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully

    Examples:
        >>> send_log_bulk("Hello", "INFO")
        True
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        # Get config from hub, fallback to from_env()
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build bulk request
        stream = oo_config.stream or "default"
        bulk_data = build_bulk_request(message, level, service_name, attributes, config, stream)

        # Send via bulk API
        url = build_bulk_url(client)

        async def _send_bulk() -> bool:
            """Send bulk request using async client."""
            response = await client._client.request(
                uri=url,
                method="POST",
                body=bulk_data,
                headers={"Content-Type": "application/x-ndjson"},
            )

            if response.is_success():
                log.debug(f"Sent log via bulk API: {message[:50]}...")
                return True
            log.debug(f"Failed to send via bulk API: {response.status}")
            return False

        return run_async(_send_bulk())

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


__all__ = [
    "build_bulk_request",
    "build_bulk_url",
    "build_log_entry",
    "send_log_bulk",
]

# 🧱🏗️🔚
