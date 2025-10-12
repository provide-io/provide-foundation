from __future__ import annotations

import contextlib
from typing import Any

"""OTLP processor for sending logs to OpenTelemetry endpoints (like OpenObserve)."""

# Check if OpenTelemetry is available
try:
    from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
    from opentelemetry.sdk._logs import LoggerProvider
    from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.semconv.resource import ResourceAttributes

    _HAS_OTEL = True
except ImportError:
    _HAS_OTEL = False
    LoggerProvider = None
    BatchLogRecordProcessor = None
    OTLPLogExporter = None
    Resource = None
    ResourceAttributes = None

# Global logger provider instance
_OTLP_LOGGER_PROVIDER: Any = None


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


def _build_otlp_headers(config: Any) -> dict[str, str]:
    """Build OTLP headers including authentication if available.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Dictionary of headers for OTLP requests

    """
    headers = dict(config.get_otlp_headers_dict())

    # Check if OpenObserve credentials are available
    try:
        from provide.foundation.integrations.openobserve.config import OpenObserveConfig

        oo_config = OpenObserveConfig.from_env()
        if oo_config.user and oo_config.password:
            # Add Basic auth header for OpenObserve
            import base64

            auth_str = f"{oo_config.user}:{oo_config.password}"
            auth_bytes = auth_str.encode("ascii")
            auth_b64 = base64.b64encode(auth_bytes).decode("ascii")
            headers["Authorization"] = f"Basic {auth_b64}"
    except ImportError:
        # OpenObserve integration not available
        pass

    return headers


def create_otlp_processor(config: Any) -> Any | None:
    """Create an OTLP processor for structlog that sends logs to OpenTelemetry.

    Args:
        config: TelemetryConfig with OTLP settings

    Returns:
        Structlog processor function or None if OTLP not available/configured

    """
    if not _HAS_OTEL:
        return None

    if not config.otlp_endpoint:
        return None

    try:
        global _OTLP_LOGGER_PROVIDER

        # Create logger provider if not already created
        if _OTLP_LOGGER_PROVIDER is None:
            # Create resource
            resource_attrs = {
                ResourceAttributes.SERVICE_NAME: config.service_name or "foundation",
            }
            if config.service_version:
                resource_attrs[ResourceAttributes.SERVICE_VERSION] = config.service_version

            resource = Resource.create(resource_attrs)

            # Configure exporter
            logs_endpoint = f"{config.otlp_endpoint}/v1/logs"
            if config.otlp_traces_endpoint:
                logs_endpoint = config.otlp_traces_endpoint.replace("/v1/traces", "/v1/logs")

            # Build headers with authentication if OpenObserve is configured
            headers = _build_otlp_headers(config)

            exporter = OTLPLogExporter(
                endpoint=logs_endpoint,
                headers=headers,
            )

            # Create provider
            _OTLP_LOGGER_PROVIDER = LoggerProvider(resource=resource)
            _OTLP_LOGGER_PROVIDER.add_log_record_processor(BatchLogRecordProcessor(exporter))

        # Get the OTLP logger
        otlp_logger = _OTLP_LOGGER_PROVIDER.get_logger(__name__)

        # Map structlog levels to OTLP severity numbers
        SEVERITY_MAP = {
            "trace": 1,
            "debug": 5,
            "info": 9,
            "warning": 13,
            "warn": 13,
            "error": 17,
            "critical": 21,
            "fatal": 21,
        }

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
                message = event_dict.get("event", "")
                level = event_dict.get("level", "info").lower()
                SEVERITY_MAP.get(level, 9)

                # Build attributes (everything except 'event' and 'timestamp')
                attributes = {k: str(v) for k, v in event_dict.items() if k not in ("event", "timestamp")}

                # Add message and level attributes for OpenObserve
                attributes["message"] = message  # Emoji-enriched message
                attributes["level"] = level.upper()  # Log level

                # Convert timestamp to nanoseconds
                timestamp = _convert_timestamp_to_nanos(event_dict.get("timestamp"))

                # Emit to OTLP using LogRecord
                from opentelemetry.sdk._logs import LogRecord

                log_record = LogRecord(
                    timestamp=timestamp,
                    observed_timestamp=timestamp,
                    trace_id=0,
                    span_id=0,
                    trace_flags=0,
                    severity_text=None,  # Not used - level is in attributes
                    severity_number=0,  # Not used - level is in attributes
                    body=None,  # No body - message is in attributes
                    resource=_OTLP_LOGGER_PROVIDER.resource,
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
    """Flush any pending OTLP logs."""
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
    """
    global _OTLP_LOGGER_PROVIDER
    if _OTLP_LOGGER_PROVIDER is not None:
        # Flush any pending logs before resetting
        flush_otlp_logs()
        _OTLP_LOGGER_PROVIDER = None
