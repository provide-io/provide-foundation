from __future__ import annotations

import logging as stdlib_logging
from typing import Any

from provide.foundation.hub import get_hub
from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.otlp_circuit import get_otlp_circuit_breaker
from provide.foundation.integrations.openobserve.otlp_helpers import (
    add_trace_attributes,
    build_bulk_url,
    build_log_entry,
    configure_otlp_exporter,
    create_otlp_resource,
    map_level_to_severity,
)
from provide.foundation.logger import get_logger
from provide.foundation.serialization import json_dumps

"""OTLP integration for sending logs to OpenObserve."""

log = get_logger(__name__)

# OpenTelemetry feature detection
try:
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
    from opentelemetry.sdk._logs import LoggerProvider
    from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.semconv.resource import ResourceAttributes

    _HAS_OTEL_LOGS = True

    # Suppress OpenTelemetry's internal error logging immediately
    # This prevents spam from BatchLogRecordProcessor's background thread
    # when OTLP endpoint is unreachable
    stdlib_logging.getLogger("opentelemetry.sdk._logs").setLevel(stdlib_logging.CRITICAL)
    stdlib_logging.getLogger("opentelemetry.sdk._shared_internal").setLevel(stdlib_logging.CRITICAL)
    stdlib_logging.getLogger("opentelemetry.exporter.otlp").setLevel(stdlib_logging.CRITICAL)
    stdlib_logging.getLogger("urllib3.connectionpool").setLevel(stdlib_logging.CRITICAL)

except ImportError:
    _HAS_OTEL_LOGS = False
    # Create mock classes for testing compatibility
    Resource = None  # type: ignore[misc,assignment]
    ResourceAttributes = None  # type: ignore[misc,assignment]
    OTLPLogExporter = None  # type: ignore[misc,assignment]
    LoggerProvider = None  # type: ignore[misc,assignment]
    BatchLogRecordProcessor = None  # type: ignore[misc,assignment]
    trace = None  # type: ignore[assignment]


def send_log_otlp(
    message: str,
    level: str = "INFO",
    service: str | None = None,
    attributes: dict[str, Any] | None = None,
) -> bool:
    """Send a log via OTLP if available.

    Uses circuit breaker pattern to prevent spam when endpoint is unreachable:
    - Tracks failure count and automatically disables OTLP after threshold
    - Implements exponential backoff for retry attempts
    - Auto-recovers after cooldown period when service is back

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

    # Check circuit breaker before attempting
    circuit_breaker = get_otlp_circuit_breaker()
    if not circuit_breaker.can_attempt():
        # Circuit is open, don't spam logs
        return False

    try:
        from provide.foundation.integrations.openobserve.config import OpenObserveConfig
        from provide.foundation.logger.config.telemetry import TelemetryConfig

        # Use initialized config from hub, fallback to from_env() for backwards compatibility
        # Only fall back if hub has no config at all, not if otlp_endpoint is missing
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        if not config.otlp_endpoint:
            return False

        # Determine service name and create resource
        actual_service_name = service or config.service_name or "foundation"
        resource = create_otlp_resource(
            actual_service_name, config.service_version, Resource, ResourceAttributes
        )

        # Configure exporter
        logs_endpoint, headers = configure_otlp_exporter(config, oo_config)
        exporter = OTLPLogExporter(endpoint=logs_endpoint, headers=headers)

        # Create logger provider
        logger_provider = LoggerProvider(resource=resource)
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))

        # Get logger and prepare attributes
        otel_logger = logger_provider.get_logger(__name__)
        log_attrs = attributes.copy() if attributes else {}
        add_trace_attributes(log_attrs, trace)

        # Map level to severity
        severity = map_level_to_severity(level)

        # Emit log record
        otel_logger.emit(  # type: ignore[call-arg]
            severity_number=severity,
            severity_text=level.upper(),
            body=message,
            attributes=log_attrs,
        )

        # Force flush to ensure delivery
        logger_provider.force_flush()

        # Record success with circuit breaker
        circuit_breaker.record_success()

        log.debug(f"Sent log via OTLP: {message[:50]}...")
        return True

    except Exception as e:
        # Record failure with circuit breaker
        circuit_breaker.record_failure(e)
        _log_otlp_failure(e, circuit_breaker, "send")
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
        from provide.foundation.integrations.openobserve.config import OpenObserveConfig
        from provide.foundation.logger.config.telemetry import TelemetryConfig
        from provide.foundation.utils.async_helpers import run_async

        if client is None:
            client = OpenObserveClient.from_config()

        # Use initialized config from hub, fallback to from_env() for backwards compatibility
        # Only fall back if hub has no config at all, preserves service_name from explicit config
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        # Build log entry
        log_entry = build_log_entry(message, level, service, attributes, config)

        # Format as bulk request
        stream = oo_config.stream or "default"
        bulk_data = json_dumps({"index": {"_index": stream}}) + "\n" + json_dumps(log_entry) + "\n"

        # Send via bulk API using Foundation transport
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
    if prefer_otlp and _HAS_OTEL_LOGS and send_log_otlp(message, level, service, attributes):
        return True

    # Fall back to bulk API
    return send_log_bulk(message, level, service, attributes, client)


def create_otlp_logger_provider() -> Any | None:
    """Create an OTLP logger provider for continuous logging.

    Uses circuit breaker to prevent spam when endpoint is unreachable.
    Returns None if circuit is open (too many failures).

    Returns:
        LoggerProvider if OTLP is available and configured, None otherwise

    """
    if not _HAS_OTEL_LOGS:
        return None

    # Check circuit breaker - don't create provider if circuit is open
    circuit_breaker = get_otlp_circuit_breaker()
    if not circuit_breaker.can_attempt():
        log.debug("OTLP circuit breaker is open, skipping logger provider creation")
        return None

    try:
        from provide.foundation.integrations.openobserve.config import OpenObserveConfig
        from provide.foundation.logger.config.telemetry import TelemetryConfig

        # Use initialized config from hub, fallback to from_env() for backwards compatibility
        # Only fall back if hub has no config at all, preserves service_name from explicit config
        hub = get_hub()
        config = hub.get_foundation_config()
        if config is None:
            config = TelemetryConfig.from_env()

        oo_config = OpenObserveConfig.from_env()

        if not config.otlp_endpoint:
            return None

        # Create resource
        resource = create_otlp_resource(
            config.service_name or "foundation",
            config.service_version,
            Resource,
            ResourceAttributes,
        )

        # Configure exporter
        logs_endpoint, headers = configure_otlp_exporter(config, oo_config)
        exporter = OTLPLogExporter(endpoint=logs_endpoint, headers=headers)

        # Create provider
        logger_provider = LoggerProvider(resource=resource)
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))

        # Record success with circuit breaker
        circuit_breaker.record_success()

        return logger_provider

    except Exception as e:
        # Record failure with circuit breaker
        circuit_breaker.record_failure(e)
        _log_otlp_failure(e, circuit_breaker, "provider creation")
        return None


def _log_otlp_failure(error: Exception, breaker: Any, context: str) -> None:
    """Log OTLP failure with circuit breaker context.

    Args:
        error: The exception that occurred
        breaker: Circuit breaker instance
        context: Context string (e.g., "send", "provider creation")
    """
    breaker_stats = breaker.get_stats()
    if breaker_stats["state"] == "open":
        log.warning(
            f"OTLP circuit breaker opened during {context}",
            failure_count=breaker_stats["failure_count"],
            timeout=breaker_stats["current_timeout"],
            error=str(error),
        )
    else:
        log.debug(
            f"OTLP {context} failed: {error}",
            circuit_state=breaker_stats["state"],
            failure_count=breaker_stats["failure_count"],
        )
