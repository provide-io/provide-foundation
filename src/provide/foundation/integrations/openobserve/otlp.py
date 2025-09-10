"""
OTLP integration for sending logs to OpenObserve.
"""

from datetime import datetime
import json
from typing import Any

from provide.foundation.logger import get_logger
from provide.foundation.integrations.openobserve.client import OpenObserveClient

log = get_logger(__name__)

# OpenTelemetry feature detection
try:
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
    from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
    from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.semconv.resource import ResourceAttributes

    _HAS_OTEL_LOGS = True
except ImportError:
    _HAS_OTEL_LOGS = False


def send_log_otlp(
    message: str,
    level: str = "INFO",
    service: str | None = None,
    attributes: dict[str, Any] | None = None,
) -> bool:
    """Send a log via OTLP if available.

    Args:
        message: Log message
        level: Log level
        service: Service name (uses config if not provided)
        attributes: Additional attributes

    Returns:
        True if sent successfully via OTLP, False otherwise
    """
    if not _HAS_OTEL_LOGS:
        return False

    try:
        from provide.foundation.logger.config import TelemetryConfig

        config = TelemetryConfig.from_env()

        if not config.otlp_endpoint:
            return False

        # Create resource with service info
        resource_attrs = {
            ResourceAttributes.SERVICE_NAME: service
            or config.service_name
            or "foundation",
        }
        if config.service_version:
            resource_attrs[ResourceAttributes.SERVICE_VERSION] = config.service_version

        resource = Resource.create(resource_attrs)

        # Configure OTLP exporter
        headers = config.get_otlp_headers_dict()
        if config.openobserve_org:
            # Add organization header for OpenObserve
            headers["organization"] = config.openobserve_org
            headers["stream-name"] = config.openobserve_stream

        # Determine endpoint for logs
        if config.otlp_traces_endpoint:
            # Replace /traces with /logs
            logs_endpoint = config.otlp_traces_endpoint.replace(
                "/v1/traces", "/v1/logs"
            )
        else:
            logs_endpoint = f"{config.otlp_endpoint}/v1/logs"

        exporter = OTLPLogExporter(
            endpoint=logs_endpoint,
            headers=headers,
        )

        # Create logger provider
        logger_provider = LoggerProvider(resource=resource)
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))

        # Get logger and emit log
        otel_logger = logger_provider.get_logger(__name__)

        # Add trace context if available
        log_attrs = attributes or {}
        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            log_attrs["trace_id"] = f"{span_context.trace_id:032x}"
            log_attrs["span_id"] = f"{span_context.span_id:016x}"

        # Map level to severity number
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
        severity = severity_map.get(level.upper(), 9)

        # Emit log record
        otel_logger.emit(
            severity_number=severity,
            severity_text=level.upper(),
            body=message,
            attributes=log_attrs,
        )

        # Force flush to ensure delivery
        logger_provider.force_flush()

        log.debug(f"Sent log via OTLP: {message[:50]}...")
        return True

    except Exception as e:
        log.debug(f"Failed to send via OTLP: {e}")
        return False


def send_log_bulk(
    message: str,
    level: str = "INFO",
    service: str | None = None,
    attributes: dict[str, Any] | None = None,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send a log via OpenObserve bulk API.

    Args:
        message: Log message
        level: Log level
        service: Service name
        attributes: Additional attributes
        client: OpenObserve client (creates new if not provided)

    Returns:
        True if sent successfully
    """
    try:
        if client is None:
            client = OpenObserveClient.from_config()

        from provide.foundation.logger.config import TelemetryConfig

        config = TelemetryConfig.from_env()

        # Build log entry
        log_entry = {
            "_timestamp": int(datetime.now().timestamp() * 1_000_000),
            "level": level.upper(),
            "message": message,
            "service": service or config.service_name or "foundation",
        }

        # Add attributes
        if attributes:
            log_entry.update(attributes)

        # Add trace context if available
        try:
            from opentelemetry import trace

            current_span = trace.get_current_span()
            if current_span and current_span.is_recording():
                span_context = current_span.get_span_context()
                log_entry["trace_id"] = f"{span_context.trace_id:032x}"
                log_entry["span_id"] = f"{span_context.span_id:016x}"
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

        # Format as bulk request
        stream = config.openobserve_stream
        bulk_data = (
            json.dumps({"index": {"_index": stream}})
            + "\n"
            + json.dumps(log_entry)
            + "\n"
        )

        # Send via bulk API
        import requests

        # Build URL - check if client.url already includes /api/{org}
        if f"/api/{client.organization}" in client.url:
            url = f"{client.url}/_bulk"
        else:
            url = f"{client.url}/api/{client.organization}/_bulk"

        response = requests.post(
            url,
            headers=client.session.headers,
            data=bulk_data,
            timeout=client.timeout,
        )

        if response.status_code == 200:
            log.debug(f"Sent log via bulk API: {message[:50]}...")
            return True
        else:
            log.debug(f"Failed to send via bulk API: {response.status_code}")
            return False

    except Exception as e:
        log.debug(f"Failed to send via bulk API: {e}")
        return False


def send_log(
    message: str,
    level: str = "INFO",
    service: str | None = None,
    attributes: dict[str, Any] | None = None,
    prefer_otlp: bool = True,
    client: OpenObserveClient | None = None,
) -> bool:
    """Send a log using OTLP if available, otherwise bulk API.

    Args:
        message: Log message
        level: Log level
        service: Service name
        attributes: Additional attributes
        prefer_otlp: Try OTLP first if True
        client: OpenObserve client for bulk API

    Returns:
        True if sent successfully
    """
    # Try OTLP first if preferred and available
    if prefer_otlp and _HAS_OTEL_LOGS:
        if send_log_otlp(message, level, service, attributes):
            return True

    # Fall back to bulk API
    return send_log_bulk(message, level, service, attributes, client)


def create_otlp_logger_provider() -> Any | None:
    """Create an OTLP logger provider for continuous logging.

    Returns:
        LoggerProvider if OTLP is available and configured, None otherwise
    """
    if not _HAS_OTEL_LOGS:
        return None

    try:
        from provide.foundation.logger.config import TelemetryConfig

        config = TelemetryConfig.from_env()

        if not config.otlp_endpoint:
            return None

        # Create resource
        resource_attrs = {
            ResourceAttributes.SERVICE_NAME: config.service_name or "foundation",
        }
        if config.service_version:
            resource_attrs[ResourceAttributes.SERVICE_VERSION] = config.service_version

        resource = Resource.create(resource_attrs)

        # Configure exporter
        headers = config.get_otlp_headers_dict()
        if config.openobserve_org:
            headers["organization"] = config.openobserve_org
            headers["stream-name"] = config.openobserve_stream

        logs_endpoint = f"{config.otlp_endpoint}/v1/logs"
        if config.otlp_traces_endpoint:
            logs_endpoint = config.otlp_traces_endpoint.replace(
                "/v1/traces", "/v1/logs"
            )

        exporter = OTLPLogExporter(
            endpoint=logs_endpoint,
            headers=headers,
        )

        # Create provider
        logger_provider = LoggerProvider(resource=resource)
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))

        return logger_provider

    except Exception as e:
        log.debug(f"Failed to create OTLP logger provider: {e}")
        return None
