# provide/foundation/logger/otlp/client.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Generic OTLP client for any OpenTelemetry-compatible backend.

Provides OTLPLogClient for sending logs via OTLP to any compatible backend
(OpenObserve, Datadog, Honeycomb, etc.).
"""

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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


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

    def xǁOTLPLogClientǁ__init____mutmut_orig(
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

    def xǁOTLPLogClientǁ__init____mutmut_1(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
        service_name: str = "XXfoundationXX",
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

    def xǁOTLPLogClientǁ__init____mutmut_2(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
        service_name: str = "FOUNDATION",
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

    def xǁOTLPLogClientǁ__init____mutmut_3(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
        service_name: str = "foundation",
        service_version: str | None = None,
        environment: str | None = None,
        timeout: float = 31.0,
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

    def xǁOTLPLogClientǁ__init____mutmut_4(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
        service_name: str = "foundation",
        service_version: str | None = None,
        environment: str | None = None,
        timeout: float = 30.0,
        use_circuit_breaker: bool = False,
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

    def xǁOTLPLogClientǁ__init____mutmut_5(
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
        self.endpoint = None
        self.headers = headers or {}
        self.service_name = service_name
        self.service_version = service_version
        self.environment = environment
        self.timeout = timeout
        self.use_circuit_breaker = use_circuit_breaker

        # Check if OpenTelemetry SDK is available
        self._otlp_available = self._check_otlp_availability()

    def xǁOTLPLogClientǁ__init____mutmut_6(
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
        self.endpoint = build_otlp_endpoint(None, signal_type="logs")
        self.headers = headers or {}
        self.service_name = service_name
        self.service_version = service_version
        self.environment = environment
        self.timeout = timeout
        self.use_circuit_breaker = use_circuit_breaker

        # Check if OpenTelemetry SDK is available
        self._otlp_available = self._check_otlp_availability()

    def xǁOTLPLogClientǁ__init____mutmut_7(
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
        self.endpoint = build_otlp_endpoint(endpoint, signal_type=None)
        self.headers = headers or {}
        self.service_name = service_name
        self.service_version = service_version
        self.environment = environment
        self.timeout = timeout
        self.use_circuit_breaker = use_circuit_breaker

        # Check if OpenTelemetry SDK is available
        self._otlp_available = self._check_otlp_availability()

    def xǁOTLPLogClientǁ__init____mutmut_8(
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
        self.endpoint = build_otlp_endpoint(signal_type="logs")
        self.headers = headers or {}
        self.service_name = service_name
        self.service_version = service_version
        self.environment = environment
        self.timeout = timeout
        self.use_circuit_breaker = use_circuit_breaker

        # Check if OpenTelemetry SDK is available
        self._otlp_available = self._check_otlp_availability()

    def xǁOTLPLogClientǁ__init____mutmut_9(
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
        self.endpoint = build_otlp_endpoint(endpoint, )
        self.headers = headers or {}
        self.service_name = service_name
        self.service_version = service_version
        self.environment = environment
        self.timeout = timeout
        self.use_circuit_breaker = use_circuit_breaker

        # Check if OpenTelemetry SDK is available
        self._otlp_available = self._check_otlp_availability()

    def xǁOTLPLogClientǁ__init____mutmut_10(
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
        self.endpoint = build_otlp_endpoint(endpoint, signal_type="XXlogsXX")
        self.headers = headers or {}
        self.service_name = service_name
        self.service_version = service_version
        self.environment = environment
        self.timeout = timeout
        self.use_circuit_breaker = use_circuit_breaker

        # Check if OpenTelemetry SDK is available
        self._otlp_available = self._check_otlp_availability()

    def xǁOTLPLogClientǁ__init____mutmut_11(
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
        self.endpoint = build_otlp_endpoint(endpoint, signal_type="LOGS")
        self.headers = headers or {}
        self.service_name = service_name
        self.service_version = service_version
        self.environment = environment
        self.timeout = timeout
        self.use_circuit_breaker = use_circuit_breaker

        # Check if OpenTelemetry SDK is available
        self._otlp_available = self._check_otlp_availability()

    def xǁOTLPLogClientǁ__init____mutmut_12(
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
        self.headers = None
        self.service_name = service_name
        self.service_version = service_version
        self.environment = environment
        self.timeout = timeout
        self.use_circuit_breaker = use_circuit_breaker

        # Check if OpenTelemetry SDK is available
        self._otlp_available = self._check_otlp_availability()

    def xǁOTLPLogClientǁ__init____mutmut_13(
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
        self.headers = headers and {}
        self.service_name = service_name
        self.service_version = service_version
        self.environment = environment
        self.timeout = timeout
        self.use_circuit_breaker = use_circuit_breaker

        # Check if OpenTelemetry SDK is available
        self._otlp_available = self._check_otlp_availability()

    def xǁOTLPLogClientǁ__init____mutmut_14(
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
        self.service_name = None
        self.service_version = service_version
        self.environment = environment
        self.timeout = timeout
        self.use_circuit_breaker = use_circuit_breaker

        # Check if OpenTelemetry SDK is available
        self._otlp_available = self._check_otlp_availability()

    def xǁOTLPLogClientǁ__init____mutmut_15(
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
        self.service_version = None
        self.environment = environment
        self.timeout = timeout
        self.use_circuit_breaker = use_circuit_breaker

        # Check if OpenTelemetry SDK is available
        self._otlp_available = self._check_otlp_availability()

    def xǁOTLPLogClientǁ__init____mutmut_16(
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
        self.environment = None
        self.timeout = timeout
        self.use_circuit_breaker = use_circuit_breaker

        # Check if OpenTelemetry SDK is available
        self._otlp_available = self._check_otlp_availability()

    def xǁOTLPLogClientǁ__init____mutmut_17(
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
        self.timeout = None
        self.use_circuit_breaker = use_circuit_breaker

        # Check if OpenTelemetry SDK is available
        self._otlp_available = self._check_otlp_availability()

    def xǁOTLPLogClientǁ__init____mutmut_18(
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
        self.use_circuit_breaker = None

        # Check if OpenTelemetry SDK is available
        self._otlp_available = self._check_otlp_availability()

    def xǁOTLPLogClientǁ__init____mutmut_19(
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
        self._otlp_available = None
    
    xǁOTLPLogClientǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOTLPLogClientǁ__init____mutmut_1': xǁOTLPLogClientǁ__init____mutmut_1, 
        'xǁOTLPLogClientǁ__init____mutmut_2': xǁOTLPLogClientǁ__init____mutmut_2, 
        'xǁOTLPLogClientǁ__init____mutmut_3': xǁOTLPLogClientǁ__init____mutmut_3, 
        'xǁOTLPLogClientǁ__init____mutmut_4': xǁOTLPLogClientǁ__init____mutmut_4, 
        'xǁOTLPLogClientǁ__init____mutmut_5': xǁOTLPLogClientǁ__init____mutmut_5, 
        'xǁOTLPLogClientǁ__init____mutmut_6': xǁOTLPLogClientǁ__init____mutmut_6, 
        'xǁOTLPLogClientǁ__init____mutmut_7': xǁOTLPLogClientǁ__init____mutmut_7, 
        'xǁOTLPLogClientǁ__init____mutmut_8': xǁOTLPLogClientǁ__init____mutmut_8, 
        'xǁOTLPLogClientǁ__init____mutmut_9': xǁOTLPLogClientǁ__init____mutmut_9, 
        'xǁOTLPLogClientǁ__init____mutmut_10': xǁOTLPLogClientǁ__init____mutmut_10, 
        'xǁOTLPLogClientǁ__init____mutmut_11': xǁOTLPLogClientǁ__init____mutmut_11, 
        'xǁOTLPLogClientǁ__init____mutmut_12': xǁOTLPLogClientǁ__init____mutmut_12, 
        'xǁOTLPLogClientǁ__init____mutmut_13': xǁOTLPLogClientǁ__init____mutmut_13, 
        'xǁOTLPLogClientǁ__init____mutmut_14': xǁOTLPLogClientǁ__init____mutmut_14, 
        'xǁOTLPLogClientǁ__init____mutmut_15': xǁOTLPLogClientǁ__init____mutmut_15, 
        'xǁOTLPLogClientǁ__init____mutmut_16': xǁOTLPLogClientǁ__init____mutmut_16, 
        'xǁOTLPLogClientǁ__init____mutmut_17': xǁOTLPLogClientǁ__init____mutmut_17, 
        'xǁOTLPLogClientǁ__init____mutmut_18': xǁOTLPLogClientǁ__init____mutmut_18, 
        'xǁOTLPLogClientǁ__init____mutmut_19': xǁOTLPLogClientǁ__init____mutmut_19
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOTLPLogClientǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁOTLPLogClientǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁOTLPLogClientǁ__init____mutmut_orig)
    xǁOTLPLogClientǁ__init____mutmut_orig.__name__ = 'xǁOTLPLogClientǁ__init__'

    def xǁOTLPLogClientǁ_check_otlp_availability__mutmut_orig(self) -> bool:
        """Check if OpenTelemetry SDK is available."""
        try:
            import opentelemetry.sdk._logs  # noqa: F401

            return True
        except ImportError:
            return False

    def xǁOTLPLogClientǁ_check_otlp_availability__mutmut_1(self) -> bool:
        """Check if OpenTelemetry SDK is available."""
        try:
            import opentelemetry.sdk._logs  # noqa: F401

            return False
        except ImportError:
            return False

    def xǁOTLPLogClientǁ_check_otlp_availability__mutmut_2(self) -> bool:
        """Check if OpenTelemetry SDK is available."""
        try:
            import opentelemetry.sdk._logs  # noqa: F401

            return True
        except ImportError:
            return True
    
    xǁOTLPLogClientǁ_check_otlp_availability__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOTLPLogClientǁ_check_otlp_availability__mutmut_1': xǁOTLPLogClientǁ_check_otlp_availability__mutmut_1, 
        'xǁOTLPLogClientǁ_check_otlp_availability__mutmut_2': xǁOTLPLogClientǁ_check_otlp_availability__mutmut_2
    }
    
    def _check_otlp_availability(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOTLPLogClientǁ_check_otlp_availability__mutmut_orig"), object.__getattribute__(self, "xǁOTLPLogClientǁ_check_otlp_availability__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _check_otlp_availability.__signature__ = _mutmut_signature(xǁOTLPLogClientǁ_check_otlp_availability__mutmut_orig)
    xǁOTLPLogClientǁ_check_otlp_availability__mutmut_orig.__name__ = 'xǁOTLPLogClientǁ_check_otlp_availability'

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

    def xǁOTLPLogClientǁsend_log__mutmut_orig(
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

    def xǁOTLPLogClientǁsend_log__mutmut_1(
        self,
        message: str,
        level: str = "XXINFOXX",
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

    def xǁOTLPLogClientǁsend_log__mutmut_2(
        self,
        message: str,
        level: str = "info",
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

    def xǁOTLPLogClientǁsend_log__mutmut_3(
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
        if self._otlp_available:
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

    def xǁOTLPLogClientǁsend_log__mutmut_4(
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
            return True

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

    def xǁOTLPLogClientǁsend_log__mutmut_5(
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
            breaker = None
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

    def xǁOTLPLogClientǁsend_log__mutmut_6(
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
            if breaker.can_attempt():
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

    def xǁOTLPLogClientǁsend_log__mutmut_7(
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
                return True

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

    def xǁOTLPLogClientǁsend_log__mutmut_8(
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
            provider = None
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

    def xǁOTLPLogClientǁsend_log__mutmut_9(
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
            if provider:
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

    def xǁOTLPLogClientǁsend_log__mutmut_10(
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
                return True

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

    def xǁOTLPLogClientǁsend_log__mutmut_11(
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
            logger = None

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

    def xǁOTLPLogClientǁsend_log__mutmut_12(
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
            logger = provider.get_logger(None)

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

    def xǁOTLPLogClientǁsend_log__mutmut_13(
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
            log_attrs = None
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

    def xǁOTLPLogClientǁsend_log__mutmut_14(
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
            add_trace_context_to_attributes(None)
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

    def xǁOTLPLogClientǁsend_log__mutmut_15(
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
            normalized_attrs = None

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

    def xǁOTLPLogClientǁsend_log__mutmut_16(
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
            normalized_attrs = normalize_attributes(None)

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

    def xǁOTLPLogClientǁsend_log__mutmut_17(
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
            severity_number = None

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

    def xǁOTLPLogClientǁsend_log__mutmut_18(
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
            severity_number = map_level_to_severity(None)

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

    def xǁOTLPLogClientǁsend_log__mutmut_19(
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
                None
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

    def xǁOTLPLogClientǁsend_log__mutmut_20(
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
                    "XXbodyXX": message,
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

    def xǁOTLPLogClientǁsend_log__mutmut_21(
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
                    "BODY": message,
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

    def xǁOTLPLogClientǁsend_log__mutmut_22(
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
                    "XXseverity_numberXX": severity_number,
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

    def xǁOTLPLogClientǁsend_log__mutmut_23(
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
                    "SEVERITY_NUMBER": severity_number,
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

    def xǁOTLPLogClientǁsend_log__mutmut_24(
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
                    "XXseverity_textXX": level.upper(),
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

    def xǁOTLPLogClientǁsend_log__mutmut_25(
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
                    "SEVERITY_TEXT": level.upper(),
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

    def xǁOTLPLogClientǁsend_log__mutmut_26(
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
                    "severity_text": level.lower(),
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

    def xǁOTLPLogClientǁsend_log__mutmut_27(
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
                    "XXattributesXX": normalized_attrs,
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

    def xǁOTLPLogClientǁsend_log__mutmut_28(
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
                    "ATTRIBUTES": normalized_attrs,
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

    def xǁOTLPLogClientǁsend_log__mutmut_29(
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
                    "XXtimestampXX": int(time.time_ns()),
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

    def xǁOTLPLogClientǁsend_log__mutmut_30(
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
                    "TIMESTAMP": int(time.time_ns()),
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

    def xǁOTLPLogClientǁsend_log__mutmut_31(
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
                    "timestamp": int(None),
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

    def xǁOTLPLogClientǁsend_log__mutmut_32(
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

            return False

        except Exception:
            if self.use_circuit_breaker:
                breaker.record_failure()
            return False

    def xǁOTLPLogClientǁsend_log__mutmut_33(
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
            return True
    
    xǁOTLPLogClientǁsend_log__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOTLPLogClientǁsend_log__mutmut_1': xǁOTLPLogClientǁsend_log__mutmut_1, 
        'xǁOTLPLogClientǁsend_log__mutmut_2': xǁOTLPLogClientǁsend_log__mutmut_2, 
        'xǁOTLPLogClientǁsend_log__mutmut_3': xǁOTLPLogClientǁsend_log__mutmut_3, 
        'xǁOTLPLogClientǁsend_log__mutmut_4': xǁOTLPLogClientǁsend_log__mutmut_4, 
        'xǁOTLPLogClientǁsend_log__mutmut_5': xǁOTLPLogClientǁsend_log__mutmut_5, 
        'xǁOTLPLogClientǁsend_log__mutmut_6': xǁOTLPLogClientǁsend_log__mutmut_6, 
        'xǁOTLPLogClientǁsend_log__mutmut_7': xǁOTLPLogClientǁsend_log__mutmut_7, 
        'xǁOTLPLogClientǁsend_log__mutmut_8': xǁOTLPLogClientǁsend_log__mutmut_8, 
        'xǁOTLPLogClientǁsend_log__mutmut_9': xǁOTLPLogClientǁsend_log__mutmut_9, 
        'xǁOTLPLogClientǁsend_log__mutmut_10': xǁOTLPLogClientǁsend_log__mutmut_10, 
        'xǁOTLPLogClientǁsend_log__mutmut_11': xǁOTLPLogClientǁsend_log__mutmut_11, 
        'xǁOTLPLogClientǁsend_log__mutmut_12': xǁOTLPLogClientǁsend_log__mutmut_12, 
        'xǁOTLPLogClientǁsend_log__mutmut_13': xǁOTLPLogClientǁsend_log__mutmut_13, 
        'xǁOTLPLogClientǁsend_log__mutmut_14': xǁOTLPLogClientǁsend_log__mutmut_14, 
        'xǁOTLPLogClientǁsend_log__mutmut_15': xǁOTLPLogClientǁsend_log__mutmut_15, 
        'xǁOTLPLogClientǁsend_log__mutmut_16': xǁOTLPLogClientǁsend_log__mutmut_16, 
        'xǁOTLPLogClientǁsend_log__mutmut_17': xǁOTLPLogClientǁsend_log__mutmut_17, 
        'xǁOTLPLogClientǁsend_log__mutmut_18': xǁOTLPLogClientǁsend_log__mutmut_18, 
        'xǁOTLPLogClientǁsend_log__mutmut_19': xǁOTLPLogClientǁsend_log__mutmut_19, 
        'xǁOTLPLogClientǁsend_log__mutmut_20': xǁOTLPLogClientǁsend_log__mutmut_20, 
        'xǁOTLPLogClientǁsend_log__mutmut_21': xǁOTLPLogClientǁsend_log__mutmut_21, 
        'xǁOTLPLogClientǁsend_log__mutmut_22': xǁOTLPLogClientǁsend_log__mutmut_22, 
        'xǁOTLPLogClientǁsend_log__mutmut_23': xǁOTLPLogClientǁsend_log__mutmut_23, 
        'xǁOTLPLogClientǁsend_log__mutmut_24': xǁOTLPLogClientǁsend_log__mutmut_24, 
        'xǁOTLPLogClientǁsend_log__mutmut_25': xǁOTLPLogClientǁsend_log__mutmut_25, 
        'xǁOTLPLogClientǁsend_log__mutmut_26': xǁOTLPLogClientǁsend_log__mutmut_26, 
        'xǁOTLPLogClientǁsend_log__mutmut_27': xǁOTLPLogClientǁsend_log__mutmut_27, 
        'xǁOTLPLogClientǁsend_log__mutmut_28': xǁOTLPLogClientǁsend_log__mutmut_28, 
        'xǁOTLPLogClientǁsend_log__mutmut_29': xǁOTLPLogClientǁsend_log__mutmut_29, 
        'xǁOTLPLogClientǁsend_log__mutmut_30': xǁOTLPLogClientǁsend_log__mutmut_30, 
        'xǁOTLPLogClientǁsend_log__mutmut_31': xǁOTLPLogClientǁsend_log__mutmut_31, 
        'xǁOTLPLogClientǁsend_log__mutmut_32': xǁOTLPLogClientǁsend_log__mutmut_32, 
        'xǁOTLPLogClientǁsend_log__mutmut_33': xǁOTLPLogClientǁsend_log__mutmut_33
    }
    
    def send_log(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOTLPLogClientǁsend_log__mutmut_orig"), object.__getattribute__(self, "xǁOTLPLogClientǁsend_log__mutmut_mutants"), args, kwargs, self)
        return result 
    
    send_log.__signature__ = _mutmut_signature(xǁOTLPLogClientǁsend_log__mutmut_orig)
    xǁOTLPLogClientǁsend_log__mutmut_orig.__name__ = 'xǁOTLPLogClientǁsend_log'

    def xǁOTLPLogClientǁcreate_logger_provider__mutmut_orig(self) -> Any | None:
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

    def xǁOTLPLogClientǁcreate_logger_provider__mutmut_1(self) -> Any | None:
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
        if self._otlp_available:
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

    def xǁOTLPLogClientǁcreate_logger_provider__mutmut_2(self) -> Any | None:
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
            breaker = None
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

    def xǁOTLPLogClientǁcreate_logger_provider__mutmut_3(self) -> Any | None:
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
            if breaker.can_attempt():
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

    def xǁOTLPLogClientǁcreate_logger_provider__mutmut_4(self) -> Any | None:
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
            provider = None
            if provider and self.use_circuit_breaker:
                breaker.record_success()
            return provider
        except Exception:
            if self.use_circuit_breaker:
                breaker.record_failure()
            return None

    def xǁOTLPLogClientǁcreate_logger_provider__mutmut_5(self) -> Any | None:
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
            if provider or self.use_circuit_breaker:
                breaker.record_success()
            return provider
        except Exception:
            if self.use_circuit_breaker:
                breaker.record_failure()
            return None
    
    xǁOTLPLogClientǁcreate_logger_provider__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOTLPLogClientǁcreate_logger_provider__mutmut_1': xǁOTLPLogClientǁcreate_logger_provider__mutmut_1, 
        'xǁOTLPLogClientǁcreate_logger_provider__mutmut_2': xǁOTLPLogClientǁcreate_logger_provider__mutmut_2, 
        'xǁOTLPLogClientǁcreate_logger_provider__mutmut_3': xǁOTLPLogClientǁcreate_logger_provider__mutmut_3, 
        'xǁOTLPLogClientǁcreate_logger_provider__mutmut_4': xǁOTLPLogClientǁcreate_logger_provider__mutmut_4, 
        'xǁOTLPLogClientǁcreate_logger_provider__mutmut_5': xǁOTLPLogClientǁcreate_logger_provider__mutmut_5
    }
    
    def create_logger_provider(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOTLPLogClientǁcreate_logger_provider__mutmut_orig"), object.__getattribute__(self, "xǁOTLPLogClientǁcreate_logger_provider__mutmut_mutants"), args, kwargs, self)
        return result 
    
    create_logger_provider.__signature__ = _mutmut_signature(xǁOTLPLogClientǁcreate_logger_provider__mutmut_orig)
    xǁOTLPLogClientǁcreate_logger_provider__mutmut_orig.__name__ = 'xǁOTLPLogClientǁcreate_logger_provider'

    def xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_orig(self) -> Any | None:
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

    def xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_1(self) -> Any | None:
        """Internal method to create logger provider."""
        try:
            from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
            from opentelemetry.sdk._logs import LoggerProvider
            from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

            # Create resource
            resource = None

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

    def xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_2(self) -> Any | None:
        """Internal method to create logger provider."""
        try:
            from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
            from opentelemetry.sdk._logs import LoggerProvider
            from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

            # Create resource
            resource = create_otlp_resource(
                service_name=None,
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

    def xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_3(self) -> Any | None:
        """Internal method to create logger provider."""
        try:
            from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
            from opentelemetry.sdk._logs import LoggerProvider
            from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

            # Create resource
            resource = create_otlp_resource(
                service_name=self.service_name,
                service_version=None,
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

    def xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_4(self) -> Any | None:
        """Internal method to create logger provider."""
        try:
            from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
            from opentelemetry.sdk._logs import LoggerProvider
            from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

            # Create resource
            resource = create_otlp_resource(
                service_name=self.service_name,
                service_version=self.service_version,
                environment=None,
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

    def xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_5(self) -> Any | None:
        """Internal method to create logger provider."""
        try:
            from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
            from opentelemetry.sdk._logs import LoggerProvider
            from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

            # Create resource
            resource = create_otlp_resource(
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

    def xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_6(self) -> Any | None:
        """Internal method to create logger provider."""
        try:
            from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
            from opentelemetry.sdk._logs import LoggerProvider
            from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

            # Create resource
            resource = create_otlp_resource(
                service_name=self.service_name,
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

    def xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_7(self) -> Any | None:
        """Internal method to create logger provider."""
        try:
            from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
            from opentelemetry.sdk._logs import LoggerProvider
            from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

            # Create resource
            resource = create_otlp_resource(
                service_name=self.service_name,
                service_version=self.service_version,
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

    def xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_8(self) -> Any | None:
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
            exporter = None

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

    def xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_9(self) -> Any | None:
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
                endpoint=None,
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

    def xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_10(self) -> Any | None:
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
                headers=None,
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

    def xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_11(self) -> Any | None:
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
                timeout=None,
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

    def xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_12(self) -> Any | None:
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

    def xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_13(self) -> Any | None:
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

    def xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_14(self) -> Any | None:
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

    def xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_15(self) -> Any | None:
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
                timeout=int(None),
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

    def xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_16(self) -> Any | None:
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
            provider = None

            # Add batch processor for efficiency
            processor = BatchLogRecordProcessor(exporter)
            provider.add_log_record_processor(processor)

            return provider

        except ImportError:
            return None
        except Exception:
            return None

    def xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_17(self) -> Any | None:
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
            provider = LoggerProvider(resource=None)

            # Add batch processor for efficiency
            processor = BatchLogRecordProcessor(exporter)
            provider.add_log_record_processor(processor)

            return provider

        except ImportError:
            return None
        except Exception:
            return None

    def xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_18(self) -> Any | None:
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
            processor = None
            provider.add_log_record_processor(processor)

            return provider

        except ImportError:
            return None
        except Exception:
            return None

    def xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_19(self) -> Any | None:
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
            processor = BatchLogRecordProcessor(None)
            provider.add_log_record_processor(processor)

            return provider

        except ImportError:
            return None
        except Exception:
            return None

    def xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_20(self) -> Any | None:
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
            provider.add_log_record_processor(None)

            return provider

        except ImportError:
            return None
        except Exception:
            return None
    
    xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_1': xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_1, 
        'xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_2': xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_2, 
        'xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_3': xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_3, 
        'xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_4': xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_4, 
        'xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_5': xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_5, 
        'xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_6': xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_6, 
        'xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_7': xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_7, 
        'xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_8': xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_8, 
        'xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_9': xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_9, 
        'xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_10': xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_10, 
        'xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_11': xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_11, 
        'xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_12': xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_12, 
        'xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_13': xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_13, 
        'xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_14': xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_14, 
        'xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_15': xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_15, 
        'xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_16': xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_16, 
        'xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_17': xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_17, 
        'xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_18': xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_18, 
        'xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_19': xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_19, 
        'xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_20': xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_20
    }
    
    def _create_logger_provider_internal(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_orig"), object.__getattribute__(self, "xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _create_logger_provider_internal.__signature__ = _mutmut_signature(xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_orig)
    xǁOTLPLogClientǁ_create_logger_provider_internal__mutmut_orig.__name__ = 'xǁOTLPLogClientǁ_create_logger_provider_internal'

    def xǁOTLPLogClientǁis_available__mutmut_orig(self) -> bool:
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

    def xǁOTLPLogClientǁis_available__mutmut_1(self) -> bool:
        """Check if OTLP is available (SDK installed and circuit not open).

        Returns:
            True if OTLP is available and circuit is closed

        Examples:
            >>> if client.is_available():
            ...     client.send_log("Message")
        """
        if self._otlp_available:
            return False

        if self.use_circuit_breaker:
            breaker = get_otlp_circuit_breaker()
            return breaker.can_attempt()

        return True

    def xǁOTLPLogClientǁis_available__mutmut_2(self) -> bool:
        """Check if OTLP is available (SDK installed and circuit not open).

        Returns:
            True if OTLP is available and circuit is closed

        Examples:
            >>> if client.is_available():
            ...     client.send_log("Message")
        """
        if not self._otlp_available:
            return True

        if self.use_circuit_breaker:
            breaker = get_otlp_circuit_breaker()
            return breaker.can_attempt()

        return True

    def xǁOTLPLogClientǁis_available__mutmut_3(self) -> bool:
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
            breaker = None
            return breaker.can_attempt()

        return True

    def xǁOTLPLogClientǁis_available__mutmut_4(self) -> bool:
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

        return False
    
    xǁOTLPLogClientǁis_available__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOTLPLogClientǁis_available__mutmut_1': xǁOTLPLogClientǁis_available__mutmut_1, 
        'xǁOTLPLogClientǁis_available__mutmut_2': xǁOTLPLogClientǁis_available__mutmut_2, 
        'xǁOTLPLogClientǁis_available__mutmut_3': xǁOTLPLogClientǁis_available__mutmut_3, 
        'xǁOTLPLogClientǁis_available__mutmut_4': xǁOTLPLogClientǁis_available__mutmut_4
    }
    
    def is_available(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOTLPLogClientǁis_available__mutmut_orig"), object.__getattribute__(self, "xǁOTLPLogClientǁis_available__mutmut_mutants"), args, kwargs, self)
        return result 
    
    is_available.__signature__ = _mutmut_signature(xǁOTLPLogClientǁis_available__mutmut_orig)
    xǁOTLPLogClientǁis_available__mutmut_orig.__name__ = 'xǁOTLPLogClientǁis_available'

    def xǁOTLPLogClientǁget_stats__mutmut_orig(self) -> dict[str, Any]:
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

    def xǁOTLPLogClientǁget_stats__mutmut_1(self) -> dict[str, Any]:
        """Get client statistics including circuit breaker state.

        Returns:
            Dictionary with client and circuit breaker statistics

        Examples:
            >>> stats = client.get_stats()
            >>> print(stats["otlp_available"])
            True
        """
        stats: dict[str, Any] = None

        if self.use_circuit_breaker:
            breaker = get_otlp_circuit_breaker()
            stats["circuit_breaker"] = breaker.get_stats()

        return stats

    def xǁOTLPLogClientǁget_stats__mutmut_2(self) -> dict[str, Any]:
        """Get client statistics including circuit breaker state.

        Returns:
            Dictionary with client and circuit breaker statistics

        Examples:
            >>> stats = client.get_stats()
            >>> print(stats["otlp_available"])
            True
        """
        stats: dict[str, Any] = {
            "XXotlp_availableXX": self._otlp_available,
            "endpoint": self.endpoint,
            "service_name": self.service_name,
        }

        if self.use_circuit_breaker:
            breaker = get_otlp_circuit_breaker()
            stats["circuit_breaker"] = breaker.get_stats()

        return stats

    def xǁOTLPLogClientǁget_stats__mutmut_3(self) -> dict[str, Any]:
        """Get client statistics including circuit breaker state.

        Returns:
            Dictionary with client and circuit breaker statistics

        Examples:
            >>> stats = client.get_stats()
            >>> print(stats["otlp_available"])
            True
        """
        stats: dict[str, Any] = {
            "OTLP_AVAILABLE": self._otlp_available,
            "endpoint": self.endpoint,
            "service_name": self.service_name,
        }

        if self.use_circuit_breaker:
            breaker = get_otlp_circuit_breaker()
            stats["circuit_breaker"] = breaker.get_stats()

        return stats

    def xǁOTLPLogClientǁget_stats__mutmut_4(self) -> dict[str, Any]:
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
            "XXendpointXX": self.endpoint,
            "service_name": self.service_name,
        }

        if self.use_circuit_breaker:
            breaker = get_otlp_circuit_breaker()
            stats["circuit_breaker"] = breaker.get_stats()

        return stats

    def xǁOTLPLogClientǁget_stats__mutmut_5(self) -> dict[str, Any]:
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
            "ENDPOINT": self.endpoint,
            "service_name": self.service_name,
        }

        if self.use_circuit_breaker:
            breaker = get_otlp_circuit_breaker()
            stats["circuit_breaker"] = breaker.get_stats()

        return stats

    def xǁOTLPLogClientǁget_stats__mutmut_6(self) -> dict[str, Any]:
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
            "XXservice_nameXX": self.service_name,
        }

        if self.use_circuit_breaker:
            breaker = get_otlp_circuit_breaker()
            stats["circuit_breaker"] = breaker.get_stats()

        return stats

    def xǁOTLPLogClientǁget_stats__mutmut_7(self) -> dict[str, Any]:
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
            "SERVICE_NAME": self.service_name,
        }

        if self.use_circuit_breaker:
            breaker = get_otlp_circuit_breaker()
            stats["circuit_breaker"] = breaker.get_stats()

        return stats

    def xǁOTLPLogClientǁget_stats__mutmut_8(self) -> dict[str, Any]:
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
            breaker = None
            stats["circuit_breaker"] = breaker.get_stats()

        return stats

    def xǁOTLPLogClientǁget_stats__mutmut_9(self) -> dict[str, Any]:
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
            stats["circuit_breaker"] = None

        return stats

    def xǁOTLPLogClientǁget_stats__mutmut_10(self) -> dict[str, Any]:
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
            stats["XXcircuit_breakerXX"] = breaker.get_stats()

        return stats

    def xǁOTLPLogClientǁget_stats__mutmut_11(self) -> dict[str, Any]:
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
            stats["CIRCUIT_BREAKER"] = breaker.get_stats()

        return stats
    
    xǁOTLPLogClientǁget_stats__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOTLPLogClientǁget_stats__mutmut_1': xǁOTLPLogClientǁget_stats__mutmut_1, 
        'xǁOTLPLogClientǁget_stats__mutmut_2': xǁOTLPLogClientǁget_stats__mutmut_2, 
        'xǁOTLPLogClientǁget_stats__mutmut_3': xǁOTLPLogClientǁget_stats__mutmut_3, 
        'xǁOTLPLogClientǁget_stats__mutmut_4': xǁOTLPLogClientǁget_stats__mutmut_4, 
        'xǁOTLPLogClientǁget_stats__mutmut_5': xǁOTLPLogClientǁget_stats__mutmut_5, 
        'xǁOTLPLogClientǁget_stats__mutmut_6': xǁOTLPLogClientǁget_stats__mutmut_6, 
        'xǁOTLPLogClientǁget_stats__mutmut_7': xǁOTLPLogClientǁget_stats__mutmut_7, 
        'xǁOTLPLogClientǁget_stats__mutmut_8': xǁOTLPLogClientǁget_stats__mutmut_8, 
        'xǁOTLPLogClientǁget_stats__mutmut_9': xǁOTLPLogClientǁget_stats__mutmut_9, 
        'xǁOTLPLogClientǁget_stats__mutmut_10': xǁOTLPLogClientǁget_stats__mutmut_10, 
        'xǁOTLPLogClientǁget_stats__mutmut_11': xǁOTLPLogClientǁget_stats__mutmut_11
    }
    
    def get_stats(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOTLPLogClientǁget_stats__mutmut_orig"), object.__getattribute__(self, "xǁOTLPLogClientǁget_stats__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_stats.__signature__ = _mutmut_signature(xǁOTLPLogClientǁget_stats__mutmut_orig)
    xǁOTLPLogClientǁget_stats__mutmut_orig.__name__ = 'xǁOTLPLogClientǁget_stats'


__all__ = [
    "OTLPLogClient",
]


# <3 🧱🤝📝🪄
