#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""OTLP processor for sending logs to OpenTelemetry endpoints.

This processor uses the generic OTLPLogClient to send logs to any OTLP-compatible backend."""

from __future__ import annotations

import contextlib
from typing import Any

from provide.foundation.logger.otlp.client import OTLPLogClient
from provide.foundation.logger.otlp.severity import map_level_to_severity

# Global logger provider instance
_OTLP_LOGGER_PROVIDER: Any | None = None


def _convert_timestamp_to_nanos(timestamp: Any) -> int | None:
    """Convert timestamp to nanoseconds for OTLP.

    Args:
        timestamp: Timestamp in various formats (string, int, float, None)

    Returns:
        Timestamp in nanoseconds or None
    """
    if not timestamp:
        return None

    if isinstance(timestamp, str):
        # Parse ISO format timestamp and convert to nanoseconds
        from datetime import datetime

        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return int(dt.timestamp() * 1_000_000_000)

    if isinstance(timestamp, (int, float)):
        # If less than year 2286 in seconds, convert to nanos; otherwise assume already nanos
        return int(timestamp * 1_000_000_000) if timestamp < 10_000_000_000 else int(timestamp)

    return None


def create_otlp_processor(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    Examples:
        >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
        >>> config = TelemetryConfig.from_env()
        >>> processor = create_otlp_processor(config)
        >>> if processor:
        ...     # Add to structlog processors
        ...     pass
    """
    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create OTLP client
            client = OTLPLogClient.from_config(config)
            if not client.is_available():
                return None

            # Create logger provider
            _OTLP_LOGGER_PROVIDER = client.create_logger_provider()
            if not _OTLP_LOGGER_PROVIDER:
                return None

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        def otlp_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
            """Structlog processor that sends logs to OTLP.

            This processor sends the log to OpenTelemetry, then returns the event_dict
            unchanged so that console output still works.

            Args:
                logger: Structlog logger instance
                method_name: Log method name (debug, info, etc.)
                event_dict: Log event dictionary

            Returns:
                Unchanged event_dict (so other processors can continue)
            """
            # Skip OTLP if explicitly flagged (e.g., for logs retrieved from OpenObserve)
            if event_dict.pop("_skip_otlp", False):
                return event_dict

            try:
                # Extract message and attributes
                message: str = str(event_dict.get("event", ""))
                level: str = str(event_dict.get("level", "info")).lower()

                # Build attributes (everything except 'event' and 'timestamp')
                attributes: dict[str, str] = {
                    k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")
                }

                # Add message and level attributes
                attributes["message"] = message
                attributes["level"] = level.upper()

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Map level to severity
                severity_number_int = map_level_to_severity(level)
                severity_text: str = level.upper()

                # Emit to OTLP using APILogRecord (new API)
                from opentelemetry.sdk._logs._internal import APILogRecord, SeverityNumber

                log_record = APILogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    context=None,
                    severity_text=severity_text,
                    severity_number=SeverityNumber(severity_number_int),
                    body=message,
                    attributes=attributes,
                )
                otlp_logger.emit(log_record)

            except Exception:
                # Silently ignore OTLP errors to not break logging
                pass

            # Return event_dict unchanged for other processors
            return event_dict

        return otlp_processor

    except Exception:
        # If OTLP setup fails, return None
        return None


def flush_otlp_logs() -> None:
    """Flush any pending OTLP logs.

    Examples:
        >>> flush_otlp_logs()
        >>> # Ensures all pending logs are sent
    """
    global _OTLP_LOGGER_PROVIDER
    if _OTLP_LOGGER_PROVIDER is not None:
        with contextlib.suppress(Exception):
            _OTLP_LOGGER_PROVIDER.force_flush(timeout_millis=5000)


def reset_otlp_provider() -> None:
    """Reset the global OTLP logger provider.

    This should be called when Foundation re-initializes to ensure
    a new LoggerProvider is created with updated configuration.
    The old provider is flushed before being reset to ensure no logs are lost.

    This is particularly important when service_name changes, as the
    OpenTelemetry Resource with service_name is immutable and baked into
    the LoggerProvider at creation time.

    Examples:
        >>> reset_otlp_provider()
        >>> # Forces recreation on next use
    """
    global _OTLP_LOGGER_PROVIDER
    if _OTLP_LOGGER_PROVIDER is not None:
        # Flush any pending logs before resetting
        flush_otlp_logs()
        _OTLP_LOGGER_PROVIDER = None


__all__ = [
    "create_otlp_processor",
    "flush_otlp_logs",
    "reset_otlp_provider",
]

# 🧱🏗️🔚
