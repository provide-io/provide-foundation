#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Generic OTLP client for any OpenTelemetry-compatible backend.

Provides OTLPLogClient for sending logs via OTLP to any compatible backend
(OpenObserve, Datadog, Honeycomb, etc.)."""

from __future__ import annotations

import logging
import time
from typing import Any

from provide.foundation.logger.otlp.circuit import get_otlp_circuit_breaker
from provide.foundation.logger.otlp.helpers import (
    add_trace_context_to_attributes,
    build_otlp_endpoint,
    normalize_attributes,
)
from provide.foundation.logger.otlp.resource import create_otlp_resource
from provide.foundation.logger.otlp.severity import map_level_to_severity

# Suppress OpenTelemetry internal logging
logging.getLogger("opentelemetry").setLevel(logging.CRITICAL)


class OTLPLogClient:
    """Generic OTLP client for any OpenTelemetry-compatible backend.

    This client works with any OTLP-compatible backend and provides:
    - Single log sending with automatic flushing
    - Persistent LoggerProvider for continuous logging
    - Circuit breaker pattern for reliability
    - Automatic trace context extraction
    - Attribute normalization for OTLP compatibility

    Examples:
        >>> client = OTLPLogClient(
        ...     endpoint="https://api.honeycomb.io/v1/logs",
        ...     headers={"x-honeycomb-team": "YOUR_API_KEY"},
        ...     service_name="my-service",
        ... )
        >>> client.send_log("Hello OTLP!", level="INFO")
        True

        >>> # Use with persistent logger provider
        >>> provider = client.create_logger_provider()
        >>> # Configure structlog to use provider
    """

    def __init__(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
        service_name: str = "foundation",
        service_version: str | None = None,
        environment: str | None = None,
        timeout: float = 30.0,
        use_circuit_breaker: bool = True,
    ) -> None:
        """Initialize OTLP client.

        Args:
            endpoint: OTLP endpoint URL (e.g., "https://api.example.com/v1/logs")
            headers: Optional custom headers (auth, organization, etc.)
            service_name: Service name for resource attributes
            service_version: Optional service version
            environment: Optional environment (dev, staging, prod)
            timeout: Request timeout in seconds
            use_circuit_breaker: Enable circuit breaker pattern
        """
        self.endpoint = build_otlp_endpoint(endpoint, signal_type="logs")
        self.headers = headers or {}
        self.service_name = service_name
        self.service_version = service_version
        self.environment = environment
        self.timeout = timeout
        self.use_circuit_breaker = use_circuit_breaker

        # Check if OpenTelemetry SDK is available
        self._otlp_available = self._check_otlp_availability()

    def _check_otlp_availability(self) -> bool:
        """Check if OpenTelemetry SDK is available."""
        try:
            import opentelemetry.sdk._logs  # noqa: F401

            return True
        except ImportError:
            return False

    @classmethod
    def from_config(
        cls,
        config: Any,
        additional_headers: dict[str, str] | None = None,
    ) -> OTLPLogClient:
        """Create client from TelemetryConfig.

        Args:
            config: TelemetryConfig instance
            additional_headers: Additional headers to merge with config headers

        Returns:
            Configured OTLPLogClient instance

        Raises:
            ValueError: If config.otlp_endpoint is not set

        Examples:
            >>> from provide.foundation.logger.config.telemetry import TelemetryConfig
            >>> config = TelemetryConfig.from_env()
            >>> client = OTLPLogClient.from_config(config)
        """
        if not config.otlp_endpoint:
            msg = "otlp_endpoint must be set in TelemetryConfig"
            raise ValueError(msg)

        headers = dict(config.otlp_headers)
        if additional_headers:
            headers.update(additional_headers)

        return cls(
            endpoint=config.otlp_endpoint,
            headers=headers,
            service_name=config.service_name or "foundation",
            service_version=config.service_version,
            environment=None,  # TODO: Add environment to TelemetryConfig
        )

    def send_log(
        self,
        message: str,
        level: str = "INFO",
        attributes: dict[str, Any] | None = None,
    ) -> bool:
        """Send single log via OTLP.

        Creates a temporary LoggerProvider, sends the log, and flushes immediately.
        This ensures delivery for single log sends but is less efficient for bulk logging.

        Args:
            message: Log message
            level: Log level (DEBUG, INFO, WARN, ERROR, FATAL)
            attributes: Optional log attributes

        Returns:
            True if sent successfully, False otherwise

        Circuit breaker pattern:
        - Checks circuit before attempting
        - Records success/failure
        - Automatically disables after threshold failures
        - Auto-recovers with exponential backoff

        Examples:
            >>> client.send_log("User logged in", level="INFO", attributes={"user_id": 123})
            True
        """
        if not self._otlp_available:
            return False

        # Check circuit breaker
        if self.use_circuit_breaker:
            breaker = get_otlp_circuit_breaker()
            if not breaker.can_attempt():
                return False

        try:
            # Create temporary logger provider
            provider = self._create_logger_provider_internal()
            if not provider:
                if self.use_circuit_breaker:
                    breaker.record_failure()
                return False

            # Get logger from provider
            logger = provider.get_logger(__name__)

            # Prepare attributes
            log_attrs = attributes.copy() if attributes else {}
            add_trace_context_to_attributes(log_attrs)
            normalized_attrs = normalize_attributes(log_attrs)

            # Map level to severity
            severity_number = map_level_to_severity(level)

            # Emit log record
            logger.emit(
                {
                    "body": message,
                    "severity_number": severity_number,
                    "severity_text": level.upper(),
                    "attributes": normalized_attrs,
                    "timestamp": int(time.time_ns()),
                }
            )

            # Force flush to ensure delivery
            provider.force_flush()

            # Shutdown provider
            provider.shutdown()

            if self.use_circuit_breaker:
                breaker.record_success()

            return True

        except Exception:
            if self.use_circuit_breaker:
                breaker.record_failure()
            return False

    def create_logger_provider(self) -> Any | None:
        """Create persistent LoggerProvider for continuous logging.

        Returns:
            LoggerProvider if OpenTelemetry SDK available, None otherwise

        Use this for long-running applications that need persistent OTLP logging.
        The provider can be used with structlog processors for automatic OTLP export.

        Circuit breaker:
        - Returns None if circuit is open
        - Records success if provider created
        - Records failure if exception occurs

        Examples:
            >>> provider = client.create_logger_provider()
            >>> if provider:
            ...     # Configure structlog with provider
            ...     pass
        """
        if not self._otlp_available:
            return None

        # Check circuit breaker
        if self.use_circuit_breaker:
            breaker = get_otlp_circuit_breaker()
            if not breaker.can_attempt():
                return None

        try:
            provider = self._create_logger_provider_internal()
            if provider and self.use_circuit_breaker:
                breaker.record_success()
            return provider
        except Exception:
            if self.use_circuit_breaker:
                breaker.record_failure()
            return None

    def _create_logger_provider_internal(self) -> Any | None:
        """Internal method to create logger provider."""
        try:
            from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
            from opentelemetry.sdk._logs import LoggerProvider
            from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

            # Create resource
            resource = create_otlp_resource(
                service_name=self.service_name,
                service_version=self.service_version,
                environment=self.environment,
            )

            # Create exporter with headers
            exporter = OTLPLogExporter(
                endpoint=self.endpoint,
                headers=self.headers,
                timeout=int(self.timeout),
            )

            # Create provider with resource
            provider = LoggerProvider(resource=resource)

            # Add batch processor for efficiency
            processor = BatchLogRecordProcessor(exporter)
            provider.add_log_record_processor(processor)

            return provider

        except ImportError:
            return None
        except Exception:
            return None

    def is_available(self) -> bool:
        """Check if OTLP is available (SDK installed and circuit not open).

        Returns:
            True if OTLP is available and circuit is closed

        Examples:
            >>> if client.is_available():
            ...     client.send_log("Message")
        """
        if not self._otlp_available:
            return False

        if self.use_circuit_breaker:
            breaker = get_otlp_circuit_breaker()
            return breaker.can_attempt()

        return True

    def get_stats(self) -> dict[str, Any]:
        """Get client statistics including circuit breaker state.

        Returns:
            Dictionary with client and circuit breaker statistics

        Examples:
            >>> stats = client.get_stats()
            >>> print(stats["otlp_available"])
            True
        """
        stats: dict[str, Any] = {
            "otlp_available": self._otlp_available,
            "endpoint": self.endpoint,
            "service_name": self.service_name,
        }

        if self.use_circuit_breaker:
            breaker = get_otlp_circuit_breaker()
            stats["circuit_breaker"] = breaker.get_stats()

        return stats


__all__ = [
    "OTLPLogClient",
]

# 🧱🏗️🔚
