# provide/foundation/metrics/otel.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from provide.foundation.logger.config.telemetry import TelemetryConfig
from provide.foundation.logger.setup import get_system_logger

if TYPE_CHECKING:
    from provide.foundation.logger.base import FoundationLogger

"""OpenTelemetry metrics integration."""

slog: FoundationLogger | Any = get_system_logger(__name__)

# Feature detection
try:
    from opentelemetry import metrics as otel_metrics
    from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
        OTLPMetricExporter as OTLPGrpcMetricExporter,
    )
    from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
        OTLPMetricExporter as OTLPHttpMetricExporter,
    )
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
    from opentelemetry.sdk.resources import Resource

    _HAS_OTEL_METRICS = True
except ImportError:
    _HAS_OTEL_METRICS = False
    # Stub everything
    otel_metrics: Any = None  # type: ignore[no-redef]
    MeterProvider: Any = None  # type: ignore[no-redef]
    PeriodicExportingMetricReader: Any = None  # type: ignore[no-redef]
    Resource: Any = None  # type: ignore[no-redef]
    OTLPGrpcMetricExporter: Any = None  # type: ignore[no-redef]
    OTLPHttpMetricExporter: Any = None  # type: ignore[no-redef]
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


def x__require_otel_metrics__mutmut_orig() -> None:
    """Ensure OpenTelemetry metrics are available."""
    if not _HAS_OTEL_METRICS:
        raise ImportError(
            "OpenTelemetry metrics require optional dependencies. "
            "Install with: pip install 'provide-foundation[opentelemetry]'",
        )


def x__require_otel_metrics__mutmut_1() -> None:
    """Ensure OpenTelemetry metrics are available."""
    if _HAS_OTEL_METRICS:
        raise ImportError(
            "OpenTelemetry metrics require optional dependencies. "
            "Install with: pip install 'provide-foundation[opentelemetry]'",
        )


def x__require_otel_metrics__mutmut_2() -> None:
    """Ensure OpenTelemetry metrics are available."""
    if not _HAS_OTEL_METRICS:
        raise ImportError(
            None,
        )


def x__require_otel_metrics__mutmut_3() -> None:
    """Ensure OpenTelemetry metrics are available."""
    if not _HAS_OTEL_METRICS:
        raise ImportError(
            "XXOpenTelemetry metrics require optional dependencies. XX"
            "Install with: pip install 'provide-foundation[opentelemetry]'",
        )


def x__require_otel_metrics__mutmut_4() -> None:
    """Ensure OpenTelemetry metrics are available."""
    if not _HAS_OTEL_METRICS:
        raise ImportError(
            "opentelemetry metrics require optional dependencies. "
            "Install with: pip install 'provide-foundation[opentelemetry]'",
        )


def x__require_otel_metrics__mutmut_5() -> None:
    """Ensure OpenTelemetry metrics are available."""
    if not _HAS_OTEL_METRICS:
        raise ImportError(
            "OPENTELEMETRY METRICS REQUIRE OPTIONAL DEPENDENCIES. "
            "Install with: pip install 'provide-foundation[opentelemetry]'",
        )


def x__require_otel_metrics__mutmut_6() -> None:
    """Ensure OpenTelemetry metrics are available."""
    if not _HAS_OTEL_METRICS:
        raise ImportError(
            "OpenTelemetry metrics require optional dependencies. "
            "XXInstall with: pip install 'provide-foundation[opentelemetry]'XX",
        )


def x__require_otel_metrics__mutmut_7() -> None:
    """Ensure OpenTelemetry metrics are available."""
    if not _HAS_OTEL_METRICS:
        raise ImportError(
            "OpenTelemetry metrics require optional dependencies. "
            "install with: pip install 'provide-foundation[opentelemetry]'",
        )


def x__require_otel_metrics__mutmut_8() -> None:
    """Ensure OpenTelemetry metrics are available."""
    if not _HAS_OTEL_METRICS:
        raise ImportError(
            "OpenTelemetry metrics require optional dependencies. "
            "INSTALL WITH: PIP INSTALL 'PROVIDE-FOUNDATION[OPENTELEMETRY]'",
        )

x__require_otel_metrics__mutmut_mutants : ClassVar[MutantDict] = {
'x__require_otel_metrics__mutmut_1': x__require_otel_metrics__mutmut_1, 
    'x__require_otel_metrics__mutmut_2': x__require_otel_metrics__mutmut_2, 
    'x__require_otel_metrics__mutmut_3': x__require_otel_metrics__mutmut_3, 
    'x__require_otel_metrics__mutmut_4': x__require_otel_metrics__mutmut_4, 
    'x__require_otel_metrics__mutmut_5': x__require_otel_metrics__mutmut_5, 
    'x__require_otel_metrics__mutmut_6': x__require_otel_metrics__mutmut_6, 
    'x__require_otel_metrics__mutmut_7': x__require_otel_metrics__mutmut_7, 
    'x__require_otel_metrics__mutmut_8': x__require_otel_metrics__mutmut_8
}

def _require_otel_metrics(*args, **kwargs):
    result = _mutmut_trampoline(x__require_otel_metrics__mutmut_orig, x__require_otel_metrics__mutmut_mutants, args, kwargs)
    return result 

_require_otel_metrics.__signature__ = _mutmut_signature(x__require_otel_metrics__mutmut_orig)
x__require_otel_metrics__mutmut_orig.__name__ = 'x__require_otel_metrics'


def x_setup_opentelemetry_metrics__mutmut_orig(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_1(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled and config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_2(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_3(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug(None)
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_4(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("XX📊 OpenTelemetry metrics disabledXX")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_5(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 opentelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_6(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OPENTELEMETRY METRICS DISABLED")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_7(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_8(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug(None)
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_9(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("XX📊 OpenTelemetry metrics not available (dependencies not installed)XX")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_10(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 opentelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_11(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OPENTELEMETRY METRICS NOT AVAILABLE (DEPENDENCIES NOT INSTALLED)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_12(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug(None)

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_13(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("XX📊🚀 Setting up OpenTelemetry metricsXX")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_14(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 setting up opentelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_15(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 SETTING UP OPENTELEMETRY METRICS")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_16(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = None
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_17(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = None
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_18(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["XXservice.nameXX"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_19(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["SERVICE.NAME"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_20(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = None

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_21(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["XXservice.versionXX"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_22(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["SERVICE.VERSION"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_23(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = None

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_24(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(None)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_25(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = None

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_26(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = None
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_27(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = None

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_28(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(None)

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_29(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol != "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_30(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "XXgrpcXX":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_31(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "GRPC":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_32(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = None
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_33(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=None,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_34(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=None,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_35(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_36(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_37(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = None

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_38(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=None,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_39(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=None,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_40(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_41(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_42(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = None
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_43(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(None, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_44(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=None)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_45(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_46(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, )
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_47(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60001)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_48(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(None)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_49(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(None)

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_50(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = None

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_51(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=None, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_52(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=None)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_53(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_54(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, )

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_55(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = None
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_56(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = None

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_57(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(None).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_58(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = None

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_59(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter") and current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_60(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"] and not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_61(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type not in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_62(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["XXNoOpMeterProviderXX", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_63(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["noopmeterprovider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_64(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NOOPMETERPROVIDER", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_65(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "XXProxyMeterProviderXX", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_66(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "proxymeterprovider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_67(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "PROXYMETERPROVIDER", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_68(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "XXMockXX", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_69(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_70(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "MOCK", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_71(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "XXMagicMockXX"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_72(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "magicmock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_73(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MAGICMOCK"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_74(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_75(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(None, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_76(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, None)
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_77(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr("get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_78(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, )
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_79(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "XXget_meterXX")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_80(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "GET_METER")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_81(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith(None)
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_82(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("XXunittest.mockXX")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_83(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("UNITTEST.MOCK")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_84(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(None)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_85(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = None
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_86(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(None)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_87(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(None)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_88(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info(None)
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_89(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("XX📊✅ OpenTelemetry metrics setup completeXX")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_90(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ opentelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_91(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OPENTELEMETRY METRICS SETUP COMPLETE")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_92(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug(None)
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_93(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("XX📊 OpenTelemetry meter provider already configuredXX")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_94(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 opentelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_95(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OPENTELEMETRY METER PROVIDER ALREADY CONFIGURED")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_96(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(None)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_97(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = None
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_98(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(None)
        _set_meter(meter)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_99(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(None)

        slog.info("📊✅ OpenTelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_100(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info(None)


def x_setup_opentelemetry_metrics__mutmut_101(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("XX📊✅ OpenTelemetry metrics setup completeXX")


def x_setup_opentelemetry_metrics__mutmut_102(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ opentelemetry metrics setup complete")


def x_setup_opentelemetry_metrics__mutmut_103(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry metrics with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if metrics are disabled first, before checking dependencies
    if not config.metrics_enabled or config.globally_disabled:
        slog.debug("📊 OpenTelemetry metrics disabled")
        return

    # Check if OpenTelemetry metrics are available
    if not _HAS_OTEL_METRICS:
        slog.debug("📊 OpenTelemetry metrics not available (dependencies not installed)")
        return

    slog.debug("📊🚀 Setting up OpenTelemetry metrics")

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Setup metric readers with OTLP exporters if configured
    readers = []

    if config.otlp_endpoint:
        endpoint = config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        slog.debug(f"📊📤 Configuring OTLP metrics exporter: {endpoint}")

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcMetricExporter | OTLPHttpMetricExporter = OTLPGrpcMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpMetricExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Create periodic reader (exports every 60 seconds by default)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        readers.append(reader)

        slog.debug(f"✅ OTLP metrics exporter configured: {config.otlp_protocol}")

    # Create meter provider
    meter_provider = MeterProvider(resource=resource, metric_readers=readers)

    # Set the global meter provider (only if not already set)
    try:
        current_provider = otel_metrics.get_meter_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own MeterProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpMeterProvider", "ProxyMeterProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "get_meter")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_metrics.set_meter_provider(meter_provider)

            # Set the global meter for our metrics module
            from provide.foundation.metrics import _set_meter

            meter = otel_metrics.get_meter(__name__)
            _set_meter(meter)

            slog.info("📊✅ OpenTelemetry metrics setup complete")
        else:
            slog.debug("📊 OpenTelemetry meter provider already configured")
    except Exception:
        # Broad catch intentional: get_meter_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_metrics.set_meter_provider(meter_provider)

        # Set the global meter for our metrics module
        from provide.foundation.metrics import _set_meter

        meter = otel_metrics.get_meter(__name__)
        _set_meter(meter)

        slog.info("📊✅ OPENTELEMETRY METRICS SETUP COMPLETE")

x_setup_opentelemetry_metrics__mutmut_mutants : ClassVar[MutantDict] = {
'x_setup_opentelemetry_metrics__mutmut_1': x_setup_opentelemetry_metrics__mutmut_1, 
    'x_setup_opentelemetry_metrics__mutmut_2': x_setup_opentelemetry_metrics__mutmut_2, 
    'x_setup_opentelemetry_metrics__mutmut_3': x_setup_opentelemetry_metrics__mutmut_3, 
    'x_setup_opentelemetry_metrics__mutmut_4': x_setup_opentelemetry_metrics__mutmut_4, 
    'x_setup_opentelemetry_metrics__mutmut_5': x_setup_opentelemetry_metrics__mutmut_5, 
    'x_setup_opentelemetry_metrics__mutmut_6': x_setup_opentelemetry_metrics__mutmut_6, 
    'x_setup_opentelemetry_metrics__mutmut_7': x_setup_opentelemetry_metrics__mutmut_7, 
    'x_setup_opentelemetry_metrics__mutmut_8': x_setup_opentelemetry_metrics__mutmut_8, 
    'x_setup_opentelemetry_metrics__mutmut_9': x_setup_opentelemetry_metrics__mutmut_9, 
    'x_setup_opentelemetry_metrics__mutmut_10': x_setup_opentelemetry_metrics__mutmut_10, 
    'x_setup_opentelemetry_metrics__mutmut_11': x_setup_opentelemetry_metrics__mutmut_11, 
    'x_setup_opentelemetry_metrics__mutmut_12': x_setup_opentelemetry_metrics__mutmut_12, 
    'x_setup_opentelemetry_metrics__mutmut_13': x_setup_opentelemetry_metrics__mutmut_13, 
    'x_setup_opentelemetry_metrics__mutmut_14': x_setup_opentelemetry_metrics__mutmut_14, 
    'x_setup_opentelemetry_metrics__mutmut_15': x_setup_opentelemetry_metrics__mutmut_15, 
    'x_setup_opentelemetry_metrics__mutmut_16': x_setup_opentelemetry_metrics__mutmut_16, 
    'x_setup_opentelemetry_metrics__mutmut_17': x_setup_opentelemetry_metrics__mutmut_17, 
    'x_setup_opentelemetry_metrics__mutmut_18': x_setup_opentelemetry_metrics__mutmut_18, 
    'x_setup_opentelemetry_metrics__mutmut_19': x_setup_opentelemetry_metrics__mutmut_19, 
    'x_setup_opentelemetry_metrics__mutmut_20': x_setup_opentelemetry_metrics__mutmut_20, 
    'x_setup_opentelemetry_metrics__mutmut_21': x_setup_opentelemetry_metrics__mutmut_21, 
    'x_setup_opentelemetry_metrics__mutmut_22': x_setup_opentelemetry_metrics__mutmut_22, 
    'x_setup_opentelemetry_metrics__mutmut_23': x_setup_opentelemetry_metrics__mutmut_23, 
    'x_setup_opentelemetry_metrics__mutmut_24': x_setup_opentelemetry_metrics__mutmut_24, 
    'x_setup_opentelemetry_metrics__mutmut_25': x_setup_opentelemetry_metrics__mutmut_25, 
    'x_setup_opentelemetry_metrics__mutmut_26': x_setup_opentelemetry_metrics__mutmut_26, 
    'x_setup_opentelemetry_metrics__mutmut_27': x_setup_opentelemetry_metrics__mutmut_27, 
    'x_setup_opentelemetry_metrics__mutmut_28': x_setup_opentelemetry_metrics__mutmut_28, 
    'x_setup_opentelemetry_metrics__mutmut_29': x_setup_opentelemetry_metrics__mutmut_29, 
    'x_setup_opentelemetry_metrics__mutmut_30': x_setup_opentelemetry_metrics__mutmut_30, 
    'x_setup_opentelemetry_metrics__mutmut_31': x_setup_opentelemetry_metrics__mutmut_31, 
    'x_setup_opentelemetry_metrics__mutmut_32': x_setup_opentelemetry_metrics__mutmut_32, 
    'x_setup_opentelemetry_metrics__mutmut_33': x_setup_opentelemetry_metrics__mutmut_33, 
    'x_setup_opentelemetry_metrics__mutmut_34': x_setup_opentelemetry_metrics__mutmut_34, 
    'x_setup_opentelemetry_metrics__mutmut_35': x_setup_opentelemetry_metrics__mutmut_35, 
    'x_setup_opentelemetry_metrics__mutmut_36': x_setup_opentelemetry_metrics__mutmut_36, 
    'x_setup_opentelemetry_metrics__mutmut_37': x_setup_opentelemetry_metrics__mutmut_37, 
    'x_setup_opentelemetry_metrics__mutmut_38': x_setup_opentelemetry_metrics__mutmut_38, 
    'x_setup_opentelemetry_metrics__mutmut_39': x_setup_opentelemetry_metrics__mutmut_39, 
    'x_setup_opentelemetry_metrics__mutmut_40': x_setup_opentelemetry_metrics__mutmut_40, 
    'x_setup_opentelemetry_metrics__mutmut_41': x_setup_opentelemetry_metrics__mutmut_41, 
    'x_setup_opentelemetry_metrics__mutmut_42': x_setup_opentelemetry_metrics__mutmut_42, 
    'x_setup_opentelemetry_metrics__mutmut_43': x_setup_opentelemetry_metrics__mutmut_43, 
    'x_setup_opentelemetry_metrics__mutmut_44': x_setup_opentelemetry_metrics__mutmut_44, 
    'x_setup_opentelemetry_metrics__mutmut_45': x_setup_opentelemetry_metrics__mutmut_45, 
    'x_setup_opentelemetry_metrics__mutmut_46': x_setup_opentelemetry_metrics__mutmut_46, 
    'x_setup_opentelemetry_metrics__mutmut_47': x_setup_opentelemetry_metrics__mutmut_47, 
    'x_setup_opentelemetry_metrics__mutmut_48': x_setup_opentelemetry_metrics__mutmut_48, 
    'x_setup_opentelemetry_metrics__mutmut_49': x_setup_opentelemetry_metrics__mutmut_49, 
    'x_setup_opentelemetry_metrics__mutmut_50': x_setup_opentelemetry_metrics__mutmut_50, 
    'x_setup_opentelemetry_metrics__mutmut_51': x_setup_opentelemetry_metrics__mutmut_51, 
    'x_setup_opentelemetry_metrics__mutmut_52': x_setup_opentelemetry_metrics__mutmut_52, 
    'x_setup_opentelemetry_metrics__mutmut_53': x_setup_opentelemetry_metrics__mutmut_53, 
    'x_setup_opentelemetry_metrics__mutmut_54': x_setup_opentelemetry_metrics__mutmut_54, 
    'x_setup_opentelemetry_metrics__mutmut_55': x_setup_opentelemetry_metrics__mutmut_55, 
    'x_setup_opentelemetry_metrics__mutmut_56': x_setup_opentelemetry_metrics__mutmut_56, 
    'x_setup_opentelemetry_metrics__mutmut_57': x_setup_opentelemetry_metrics__mutmut_57, 
    'x_setup_opentelemetry_metrics__mutmut_58': x_setup_opentelemetry_metrics__mutmut_58, 
    'x_setup_opentelemetry_metrics__mutmut_59': x_setup_opentelemetry_metrics__mutmut_59, 
    'x_setup_opentelemetry_metrics__mutmut_60': x_setup_opentelemetry_metrics__mutmut_60, 
    'x_setup_opentelemetry_metrics__mutmut_61': x_setup_opentelemetry_metrics__mutmut_61, 
    'x_setup_opentelemetry_metrics__mutmut_62': x_setup_opentelemetry_metrics__mutmut_62, 
    'x_setup_opentelemetry_metrics__mutmut_63': x_setup_opentelemetry_metrics__mutmut_63, 
    'x_setup_opentelemetry_metrics__mutmut_64': x_setup_opentelemetry_metrics__mutmut_64, 
    'x_setup_opentelemetry_metrics__mutmut_65': x_setup_opentelemetry_metrics__mutmut_65, 
    'x_setup_opentelemetry_metrics__mutmut_66': x_setup_opentelemetry_metrics__mutmut_66, 
    'x_setup_opentelemetry_metrics__mutmut_67': x_setup_opentelemetry_metrics__mutmut_67, 
    'x_setup_opentelemetry_metrics__mutmut_68': x_setup_opentelemetry_metrics__mutmut_68, 
    'x_setup_opentelemetry_metrics__mutmut_69': x_setup_opentelemetry_metrics__mutmut_69, 
    'x_setup_opentelemetry_metrics__mutmut_70': x_setup_opentelemetry_metrics__mutmut_70, 
    'x_setup_opentelemetry_metrics__mutmut_71': x_setup_opentelemetry_metrics__mutmut_71, 
    'x_setup_opentelemetry_metrics__mutmut_72': x_setup_opentelemetry_metrics__mutmut_72, 
    'x_setup_opentelemetry_metrics__mutmut_73': x_setup_opentelemetry_metrics__mutmut_73, 
    'x_setup_opentelemetry_metrics__mutmut_74': x_setup_opentelemetry_metrics__mutmut_74, 
    'x_setup_opentelemetry_metrics__mutmut_75': x_setup_opentelemetry_metrics__mutmut_75, 
    'x_setup_opentelemetry_metrics__mutmut_76': x_setup_opentelemetry_metrics__mutmut_76, 
    'x_setup_opentelemetry_metrics__mutmut_77': x_setup_opentelemetry_metrics__mutmut_77, 
    'x_setup_opentelemetry_metrics__mutmut_78': x_setup_opentelemetry_metrics__mutmut_78, 
    'x_setup_opentelemetry_metrics__mutmut_79': x_setup_opentelemetry_metrics__mutmut_79, 
    'x_setup_opentelemetry_metrics__mutmut_80': x_setup_opentelemetry_metrics__mutmut_80, 
    'x_setup_opentelemetry_metrics__mutmut_81': x_setup_opentelemetry_metrics__mutmut_81, 
    'x_setup_opentelemetry_metrics__mutmut_82': x_setup_opentelemetry_metrics__mutmut_82, 
    'x_setup_opentelemetry_metrics__mutmut_83': x_setup_opentelemetry_metrics__mutmut_83, 
    'x_setup_opentelemetry_metrics__mutmut_84': x_setup_opentelemetry_metrics__mutmut_84, 
    'x_setup_opentelemetry_metrics__mutmut_85': x_setup_opentelemetry_metrics__mutmut_85, 
    'x_setup_opentelemetry_metrics__mutmut_86': x_setup_opentelemetry_metrics__mutmut_86, 
    'x_setup_opentelemetry_metrics__mutmut_87': x_setup_opentelemetry_metrics__mutmut_87, 
    'x_setup_opentelemetry_metrics__mutmut_88': x_setup_opentelemetry_metrics__mutmut_88, 
    'x_setup_opentelemetry_metrics__mutmut_89': x_setup_opentelemetry_metrics__mutmut_89, 
    'x_setup_opentelemetry_metrics__mutmut_90': x_setup_opentelemetry_metrics__mutmut_90, 
    'x_setup_opentelemetry_metrics__mutmut_91': x_setup_opentelemetry_metrics__mutmut_91, 
    'x_setup_opentelemetry_metrics__mutmut_92': x_setup_opentelemetry_metrics__mutmut_92, 
    'x_setup_opentelemetry_metrics__mutmut_93': x_setup_opentelemetry_metrics__mutmut_93, 
    'x_setup_opentelemetry_metrics__mutmut_94': x_setup_opentelemetry_metrics__mutmut_94, 
    'x_setup_opentelemetry_metrics__mutmut_95': x_setup_opentelemetry_metrics__mutmut_95, 
    'x_setup_opentelemetry_metrics__mutmut_96': x_setup_opentelemetry_metrics__mutmut_96, 
    'x_setup_opentelemetry_metrics__mutmut_97': x_setup_opentelemetry_metrics__mutmut_97, 
    'x_setup_opentelemetry_metrics__mutmut_98': x_setup_opentelemetry_metrics__mutmut_98, 
    'x_setup_opentelemetry_metrics__mutmut_99': x_setup_opentelemetry_metrics__mutmut_99, 
    'x_setup_opentelemetry_metrics__mutmut_100': x_setup_opentelemetry_metrics__mutmut_100, 
    'x_setup_opentelemetry_metrics__mutmut_101': x_setup_opentelemetry_metrics__mutmut_101, 
    'x_setup_opentelemetry_metrics__mutmut_102': x_setup_opentelemetry_metrics__mutmut_102, 
    'x_setup_opentelemetry_metrics__mutmut_103': x_setup_opentelemetry_metrics__mutmut_103
}

def setup_opentelemetry_metrics(*args, **kwargs):
    result = _mutmut_trampoline(x_setup_opentelemetry_metrics__mutmut_orig, x_setup_opentelemetry_metrics__mutmut_mutants, args, kwargs)
    return result 

setup_opentelemetry_metrics.__signature__ = _mutmut_signature(x_setup_opentelemetry_metrics__mutmut_orig)
x_setup_opentelemetry_metrics__mutmut_orig.__name__ = 'x_setup_opentelemetry_metrics'


def x_shutdown_opentelemetry_metrics__mutmut_orig() -> None:
    """Shutdown OpenTelemetry metrics."""
    if not _HAS_OTEL_METRICS:
        return

    try:
        meter_provider = otel_metrics.get_meter_provider()
        if hasattr(meter_provider, "shutdown"):
            meter_provider.shutdown()
            slog.debug("📊🛑 OpenTelemetry meter provider shutdown")
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry metrics: {e}")


def x_shutdown_opentelemetry_metrics__mutmut_1() -> None:
    """Shutdown OpenTelemetry metrics."""
    if _HAS_OTEL_METRICS:
        return

    try:
        meter_provider = otel_metrics.get_meter_provider()
        if hasattr(meter_provider, "shutdown"):
            meter_provider.shutdown()
            slog.debug("📊🛑 OpenTelemetry meter provider shutdown")
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry metrics: {e}")


def x_shutdown_opentelemetry_metrics__mutmut_2() -> None:
    """Shutdown OpenTelemetry metrics."""
    if not _HAS_OTEL_METRICS:
        return

    try:
        meter_provider = None
        if hasattr(meter_provider, "shutdown"):
            meter_provider.shutdown()
            slog.debug("📊🛑 OpenTelemetry meter provider shutdown")
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry metrics: {e}")


def x_shutdown_opentelemetry_metrics__mutmut_3() -> None:
    """Shutdown OpenTelemetry metrics."""
    if not _HAS_OTEL_METRICS:
        return

    try:
        meter_provider = otel_metrics.get_meter_provider()
        if hasattr(None, "shutdown"):
            meter_provider.shutdown()
            slog.debug("📊🛑 OpenTelemetry meter provider shutdown")
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry metrics: {e}")


def x_shutdown_opentelemetry_metrics__mutmut_4() -> None:
    """Shutdown OpenTelemetry metrics."""
    if not _HAS_OTEL_METRICS:
        return

    try:
        meter_provider = otel_metrics.get_meter_provider()
        if hasattr(meter_provider, None):
            meter_provider.shutdown()
            slog.debug("📊🛑 OpenTelemetry meter provider shutdown")
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry metrics: {e}")


def x_shutdown_opentelemetry_metrics__mutmut_5() -> None:
    """Shutdown OpenTelemetry metrics."""
    if not _HAS_OTEL_METRICS:
        return

    try:
        meter_provider = otel_metrics.get_meter_provider()
        if hasattr("shutdown"):
            meter_provider.shutdown()
            slog.debug("📊🛑 OpenTelemetry meter provider shutdown")
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry metrics: {e}")


def x_shutdown_opentelemetry_metrics__mutmut_6() -> None:
    """Shutdown OpenTelemetry metrics."""
    if not _HAS_OTEL_METRICS:
        return

    try:
        meter_provider = otel_metrics.get_meter_provider()
        if hasattr(meter_provider, ):
            meter_provider.shutdown()
            slog.debug("📊🛑 OpenTelemetry meter provider shutdown")
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry metrics: {e}")


def x_shutdown_opentelemetry_metrics__mutmut_7() -> None:
    """Shutdown OpenTelemetry metrics."""
    if not _HAS_OTEL_METRICS:
        return

    try:
        meter_provider = otel_metrics.get_meter_provider()
        if hasattr(meter_provider, "XXshutdownXX"):
            meter_provider.shutdown()
            slog.debug("📊🛑 OpenTelemetry meter provider shutdown")
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry metrics: {e}")


def x_shutdown_opentelemetry_metrics__mutmut_8() -> None:
    """Shutdown OpenTelemetry metrics."""
    if not _HAS_OTEL_METRICS:
        return

    try:
        meter_provider = otel_metrics.get_meter_provider()
        if hasattr(meter_provider, "SHUTDOWN"):
            meter_provider.shutdown()
            slog.debug("📊🛑 OpenTelemetry meter provider shutdown")
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry metrics: {e}")


def x_shutdown_opentelemetry_metrics__mutmut_9() -> None:
    """Shutdown OpenTelemetry metrics."""
    if not _HAS_OTEL_METRICS:
        return

    try:
        meter_provider = otel_metrics.get_meter_provider()
        if hasattr(meter_provider, "shutdown"):
            meter_provider.shutdown()
            slog.debug(None)
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry metrics: {e}")


def x_shutdown_opentelemetry_metrics__mutmut_10() -> None:
    """Shutdown OpenTelemetry metrics."""
    if not _HAS_OTEL_METRICS:
        return

    try:
        meter_provider = otel_metrics.get_meter_provider()
        if hasattr(meter_provider, "shutdown"):
            meter_provider.shutdown()
            slog.debug("XX📊🛑 OpenTelemetry meter provider shutdownXX")
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry metrics: {e}")


def x_shutdown_opentelemetry_metrics__mutmut_11() -> None:
    """Shutdown OpenTelemetry metrics."""
    if not _HAS_OTEL_METRICS:
        return

    try:
        meter_provider = otel_metrics.get_meter_provider()
        if hasattr(meter_provider, "shutdown"):
            meter_provider.shutdown()
            slog.debug("📊🛑 opentelemetry meter provider shutdown")
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry metrics: {e}")


def x_shutdown_opentelemetry_metrics__mutmut_12() -> None:
    """Shutdown OpenTelemetry metrics."""
    if not _HAS_OTEL_METRICS:
        return

    try:
        meter_provider = otel_metrics.get_meter_provider()
        if hasattr(meter_provider, "shutdown"):
            meter_provider.shutdown()
            slog.debug("📊🛑 OPENTELEMETRY METER PROVIDER SHUTDOWN")
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry metrics: {e}")


def x_shutdown_opentelemetry_metrics__mutmut_13() -> None:
    """Shutdown OpenTelemetry metrics."""
    if not _HAS_OTEL_METRICS:
        return

    try:
        meter_provider = otel_metrics.get_meter_provider()
        if hasattr(meter_provider, "shutdown"):
            meter_provider.shutdown()
            slog.debug("📊🛑 OpenTelemetry meter provider shutdown")
    except Exception as e:
        slog.warning(None)

x_shutdown_opentelemetry_metrics__mutmut_mutants : ClassVar[MutantDict] = {
'x_shutdown_opentelemetry_metrics__mutmut_1': x_shutdown_opentelemetry_metrics__mutmut_1, 
    'x_shutdown_opentelemetry_metrics__mutmut_2': x_shutdown_opentelemetry_metrics__mutmut_2, 
    'x_shutdown_opentelemetry_metrics__mutmut_3': x_shutdown_opentelemetry_metrics__mutmut_3, 
    'x_shutdown_opentelemetry_metrics__mutmut_4': x_shutdown_opentelemetry_metrics__mutmut_4, 
    'x_shutdown_opentelemetry_metrics__mutmut_5': x_shutdown_opentelemetry_metrics__mutmut_5, 
    'x_shutdown_opentelemetry_metrics__mutmut_6': x_shutdown_opentelemetry_metrics__mutmut_6, 
    'x_shutdown_opentelemetry_metrics__mutmut_7': x_shutdown_opentelemetry_metrics__mutmut_7, 
    'x_shutdown_opentelemetry_metrics__mutmut_8': x_shutdown_opentelemetry_metrics__mutmut_8, 
    'x_shutdown_opentelemetry_metrics__mutmut_9': x_shutdown_opentelemetry_metrics__mutmut_9, 
    'x_shutdown_opentelemetry_metrics__mutmut_10': x_shutdown_opentelemetry_metrics__mutmut_10, 
    'x_shutdown_opentelemetry_metrics__mutmut_11': x_shutdown_opentelemetry_metrics__mutmut_11, 
    'x_shutdown_opentelemetry_metrics__mutmut_12': x_shutdown_opentelemetry_metrics__mutmut_12, 
    'x_shutdown_opentelemetry_metrics__mutmut_13': x_shutdown_opentelemetry_metrics__mutmut_13
}

def shutdown_opentelemetry_metrics(*args, **kwargs):
    result = _mutmut_trampoline(x_shutdown_opentelemetry_metrics__mutmut_orig, x_shutdown_opentelemetry_metrics__mutmut_mutants, args, kwargs)
    return result 

shutdown_opentelemetry_metrics.__signature__ = _mutmut_signature(x_shutdown_opentelemetry_metrics__mutmut_orig)
x_shutdown_opentelemetry_metrics__mutmut_orig.__name__ = 'x_shutdown_opentelemetry_metrics'


# <3 🧱🤝📈🪄
