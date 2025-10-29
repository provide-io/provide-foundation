# provide/foundation/tracer/otel.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from provide.foundation.logger.config.telemetry import TelemetryConfig
from provide.foundation.logger.setup import get_system_logger

if TYPE_CHECKING:
    from opentelemetry import trace as otel_trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
        OTLPSpanExporter as OTLPGrpcSpanExporter,
    )
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
        OTLPSpanExporter as OTLPHttpSpanExporter,
    )
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.trace.sampling import TraceIdRatioBased

    from provide.foundation.logger.base import FoundationLogger

"""OpenTelemetry integration for Foundation tracer."""

slog: FoundationLogger | Any = get_system_logger(__name__)

# Feature detection
try:
    from opentelemetry import trace as otel_trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
        OTLPSpanExporter as OTLPGrpcSpanExporter,
    )
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
        OTLPSpanExporter as OTLPHttpSpanExporter,
    )
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.trace.sampling import TraceIdRatioBased

    _HAS_OTEL = True
except ImportError:
    _HAS_OTEL = False
    # Stub everything for type hints
    otel_trace: Any = None  # type: ignore[no-redef]
    TracerProvider: Any = None  # type: ignore[no-redef]
    BatchSpanProcessor: Any = None  # type: ignore[no-redef]
    Resource: Any = None  # type: ignore[no-redef]
    OTLPGrpcSpanExporter: Any = None  # type: ignore[no-redef]
    OTLPHttpSpanExporter: Any = None  # type: ignore[no-redef]
    TraceIdRatioBased: Any = None  # type: ignore[no-redef]
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x__require_otel__mutmut_orig() -> None:
    """Ensure OpenTelemetry is available."""
    if not _HAS_OTEL:
        raise ImportError(
            "OpenTelemetry features require optional dependencies. "
            "Install with: pip install 'provide-foundation[opentelemetry]'",
        )


def x__require_otel__mutmut_1() -> None:
    """Ensure OpenTelemetry is available."""
    if _HAS_OTEL:
        raise ImportError(
            "OpenTelemetry features require optional dependencies. "
            "Install with: pip install 'provide-foundation[opentelemetry]'",
        )


def x__require_otel__mutmut_2() -> None:
    """Ensure OpenTelemetry is available."""
    if not _HAS_OTEL:
        raise ImportError(
            None,
        )


def x__require_otel__mutmut_3() -> None:
    """Ensure OpenTelemetry is available."""
    if not _HAS_OTEL:
        raise ImportError(
            "XXOpenTelemetry features require optional dependencies. XX"
            "Install with: pip install 'provide-foundation[opentelemetry]'",
        )


def x__require_otel__mutmut_4() -> None:
    """Ensure OpenTelemetry is available."""
    if not _HAS_OTEL:
        raise ImportError(
            "opentelemetry features require optional dependencies. "
            "Install with: pip install 'provide-foundation[opentelemetry]'",
        )


def x__require_otel__mutmut_5() -> None:
    """Ensure OpenTelemetry is available."""
    if not _HAS_OTEL:
        raise ImportError(
            "OPENTELEMETRY FEATURES REQUIRE OPTIONAL DEPENDENCIES. "
            "Install with: pip install 'provide-foundation[opentelemetry]'",
        )


def x__require_otel__mutmut_6() -> None:
    """Ensure OpenTelemetry is available."""
    if not _HAS_OTEL:
        raise ImportError(
            "OpenTelemetry features require optional dependencies. "
            "XXInstall with: pip install 'provide-foundation[opentelemetry]'XX",
        )


def x__require_otel__mutmut_7() -> None:
    """Ensure OpenTelemetry is available."""
    if not _HAS_OTEL:
        raise ImportError(
            "OpenTelemetry features require optional dependencies. "
            "install with: pip install 'provide-foundation[opentelemetry]'",
        )


def x__require_otel__mutmut_8() -> None:
    """Ensure OpenTelemetry is available."""
    if not _HAS_OTEL:
        raise ImportError(
            "OpenTelemetry features require optional dependencies. "
            "INSTALL WITH: PIP INSTALL 'PROVIDE-FOUNDATION[OPENTELEMETRY]'",
        )


x__require_otel__mutmut_mutants: ClassVar[MutantDict] = {
    "x__require_otel__mutmut_1": x__require_otel__mutmut_1,
    "x__require_otel__mutmut_2": x__require_otel__mutmut_2,
    "x__require_otel__mutmut_3": x__require_otel__mutmut_3,
    "x__require_otel__mutmut_4": x__require_otel__mutmut_4,
    "x__require_otel__mutmut_5": x__require_otel__mutmut_5,
    "x__require_otel__mutmut_6": x__require_otel__mutmut_6,
    "x__require_otel__mutmut_7": x__require_otel__mutmut_7,
    "x__require_otel__mutmut_8": x__require_otel__mutmut_8,
}


def _require_otel(*args, **kwargs):
    result = _mutmut_trampoline(x__require_otel__mutmut_orig, x__require_otel__mutmut_mutants, args, kwargs)
    return result


_require_otel.__signature__ = _mutmut_signature(x__require_otel__mutmut_orig)
x__require_otel__mutmut_orig.__name__ = "x__require_otel"


def x_setup_opentelemetry_tracing__mutmut_orig(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_1(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled and config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_2(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_3(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_4(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = None
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_5(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = None
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_6(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["XXservice.nameXX"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_7(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["SERVICE.NAME"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_8(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = None

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_9(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["XXservice.versionXX"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_10(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["SERVICE.VERSION"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_11(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = None

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_12(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(None)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_13(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = None
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_14(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(None)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_15(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = None

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_16(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=None, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_17(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=None)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_18(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_19(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(
        resource=resource,
    )

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_20(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint and config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_21(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = None
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_22(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint and config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_23(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = None

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_24(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol != "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_25(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "XXgrpcXX":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_26(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "GRPC":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_27(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = None
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_28(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=None,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_29(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=None,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_30(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_31(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_32(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = None

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_33(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=None,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_34(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=None,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_35(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_36(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_37(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = None
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_38(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(None)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_39(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(None)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_40(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(None)

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_41(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = None
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_42(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = None

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_43(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(None).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_44(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = None

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_45(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            and current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_46(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            and not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_47(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type not in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_48(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["XXNoOpTracerProviderXX", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_49(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["nooptracerprovider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_50(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NOOPTRACERPROVIDER", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_51(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "XXProxyTracerProviderXX", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_52(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "proxytracerprovider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_53(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "PROXYTRACERPROVIDER", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_54(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "XXMockXX", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_55(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_56(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "MOCK", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_57(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "XXMagicMockXX"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_58(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "magicmock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_59(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MAGICMOCK"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_60(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_61(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(None, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_62(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, None)
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_63(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr("add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_64(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(
                current_provider,
            )
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_65(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "XXadd_span_processorXX")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_66(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "ADD_SPAN_PROCESSOR")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_67(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith(None)
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_68(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("XXunittest.mockXX")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_69(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("UNITTEST.MOCK")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_70(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(None)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_71(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info(None)
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_72(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("XX🔍✅ OpenTelemetry tracing setup completeXX")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_73(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ opentelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_74(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OPENTELEMETRY TRACING SETUP COMPLETE")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_75(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug(None)
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_76(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("XX🔍 OpenTelemetry tracer provider already configuredXX")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_77(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 opentelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_78(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OPENTELEMETRY TRACER PROVIDER ALREADY CONFIGURED")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_79(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(None)
        slog.info("🔍✅ OpenTelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_80(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info(None)


def x_setup_opentelemetry_tracing__mutmut_81(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("XX🔍✅ OpenTelemetry tracing setup completeXX")


def x_setup_opentelemetry_tracing__mutmut_82(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ opentelemetry tracing setup complete")


def x_setup_opentelemetry_tracing__mutmut_83(config: TelemetryConfig) -> None:
    """Setup OpenTelemetry tracing with configuration.

    Args:
        config: Telemetry configuration

    """
    # Check if tracing is disabled first, before checking dependencies
    if not config.tracing_enabled or config.globally_disabled:
        return

    # Check if OpenTelemetry is available
    if not _HAS_OTEL:
        return

    # Create resource with service information
    resource_attrs = {}
    if config.service_name:
        resource_attrs["service.name"] = config.service_name
    if config.service_version:
        resource_attrs["service.version"] = config.service_version

    resource = Resource.create(resource_attrs)

    # Create tracer provider with sampling
    sampler = TraceIdRatioBased(config.trace_sample_rate)
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)

    # Setup OTLP exporter if endpoint is configured
    if config.otlp_endpoint or config.otlp_traces_endpoint:
        endpoint = config.otlp_traces_endpoint or config.otlp_endpoint
        headers = config.get_otlp_headers_dict()

        # Configuring OTLP exporter

        # Choose exporter based on protocol
        if config.otlp_protocol == "grpc":
            exporter: OTLPGrpcSpanExporter | OTLPHttpSpanExporter = OTLPGrpcSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )
        else:  # http/protobuf
            exporter = OTLPHttpSpanExporter(
                endpoint=endpoint,
                headers=headers,
            )

        # Add batch processor
        processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(processor)

        slog.debug(f"✅ OTLP span exporter configured: {config.otlp_protocol}")

    # Set the global tracer provider (only if not already set)
    try:
        current_provider = otel_trace.get_tracer_provider()
        provider_type = type(current_provider).__name__

        # Always allow setup if:
        # 1. It's a default/no-op provider
        # 2. It's a mock (for testing)
        # 3. It's our own TracerProvider type (allow re-configuration)
        should_setup = (
            provider_type in ["NoOpTracerProvider", "ProxyTracerProvider", "Mock", "MagicMock"]
            or not hasattr(current_provider, "add_span_processor")
            or current_provider.__class__.__module__.startswith("unittest.mock")
        )

        if should_setup:
            otel_trace.set_tracer_provider(tracer_provider)
            slog.info("🔍✅ OpenTelemetry tracing setup complete")
        else:
            slog.debug("🔍 OpenTelemetry tracer provider already configured")
    except Exception:
        # Broad catch intentional: get_tracer_provider() may fail in various OTEL environments
        # Proceed with setup if provider check fails
        otel_trace.set_tracer_provider(tracer_provider)
        slog.info("🔍✅ OPENTELEMETRY TRACING SETUP COMPLETE")


x_setup_opentelemetry_tracing__mutmut_mutants: ClassVar[MutantDict] = {
    "x_setup_opentelemetry_tracing__mutmut_1": x_setup_opentelemetry_tracing__mutmut_1,
    "x_setup_opentelemetry_tracing__mutmut_2": x_setup_opentelemetry_tracing__mutmut_2,
    "x_setup_opentelemetry_tracing__mutmut_3": x_setup_opentelemetry_tracing__mutmut_3,
    "x_setup_opentelemetry_tracing__mutmut_4": x_setup_opentelemetry_tracing__mutmut_4,
    "x_setup_opentelemetry_tracing__mutmut_5": x_setup_opentelemetry_tracing__mutmut_5,
    "x_setup_opentelemetry_tracing__mutmut_6": x_setup_opentelemetry_tracing__mutmut_6,
    "x_setup_opentelemetry_tracing__mutmut_7": x_setup_opentelemetry_tracing__mutmut_7,
    "x_setup_opentelemetry_tracing__mutmut_8": x_setup_opentelemetry_tracing__mutmut_8,
    "x_setup_opentelemetry_tracing__mutmut_9": x_setup_opentelemetry_tracing__mutmut_9,
    "x_setup_opentelemetry_tracing__mutmut_10": x_setup_opentelemetry_tracing__mutmut_10,
    "x_setup_opentelemetry_tracing__mutmut_11": x_setup_opentelemetry_tracing__mutmut_11,
    "x_setup_opentelemetry_tracing__mutmut_12": x_setup_opentelemetry_tracing__mutmut_12,
    "x_setup_opentelemetry_tracing__mutmut_13": x_setup_opentelemetry_tracing__mutmut_13,
    "x_setup_opentelemetry_tracing__mutmut_14": x_setup_opentelemetry_tracing__mutmut_14,
    "x_setup_opentelemetry_tracing__mutmut_15": x_setup_opentelemetry_tracing__mutmut_15,
    "x_setup_opentelemetry_tracing__mutmut_16": x_setup_opentelemetry_tracing__mutmut_16,
    "x_setup_opentelemetry_tracing__mutmut_17": x_setup_opentelemetry_tracing__mutmut_17,
    "x_setup_opentelemetry_tracing__mutmut_18": x_setup_opentelemetry_tracing__mutmut_18,
    "x_setup_opentelemetry_tracing__mutmut_19": x_setup_opentelemetry_tracing__mutmut_19,
    "x_setup_opentelemetry_tracing__mutmut_20": x_setup_opentelemetry_tracing__mutmut_20,
    "x_setup_opentelemetry_tracing__mutmut_21": x_setup_opentelemetry_tracing__mutmut_21,
    "x_setup_opentelemetry_tracing__mutmut_22": x_setup_opentelemetry_tracing__mutmut_22,
    "x_setup_opentelemetry_tracing__mutmut_23": x_setup_opentelemetry_tracing__mutmut_23,
    "x_setup_opentelemetry_tracing__mutmut_24": x_setup_opentelemetry_tracing__mutmut_24,
    "x_setup_opentelemetry_tracing__mutmut_25": x_setup_opentelemetry_tracing__mutmut_25,
    "x_setup_opentelemetry_tracing__mutmut_26": x_setup_opentelemetry_tracing__mutmut_26,
    "x_setup_opentelemetry_tracing__mutmut_27": x_setup_opentelemetry_tracing__mutmut_27,
    "x_setup_opentelemetry_tracing__mutmut_28": x_setup_opentelemetry_tracing__mutmut_28,
    "x_setup_opentelemetry_tracing__mutmut_29": x_setup_opentelemetry_tracing__mutmut_29,
    "x_setup_opentelemetry_tracing__mutmut_30": x_setup_opentelemetry_tracing__mutmut_30,
    "x_setup_opentelemetry_tracing__mutmut_31": x_setup_opentelemetry_tracing__mutmut_31,
    "x_setup_opentelemetry_tracing__mutmut_32": x_setup_opentelemetry_tracing__mutmut_32,
    "x_setup_opentelemetry_tracing__mutmut_33": x_setup_opentelemetry_tracing__mutmut_33,
    "x_setup_opentelemetry_tracing__mutmut_34": x_setup_opentelemetry_tracing__mutmut_34,
    "x_setup_opentelemetry_tracing__mutmut_35": x_setup_opentelemetry_tracing__mutmut_35,
    "x_setup_opentelemetry_tracing__mutmut_36": x_setup_opentelemetry_tracing__mutmut_36,
    "x_setup_opentelemetry_tracing__mutmut_37": x_setup_opentelemetry_tracing__mutmut_37,
    "x_setup_opentelemetry_tracing__mutmut_38": x_setup_opentelemetry_tracing__mutmut_38,
    "x_setup_opentelemetry_tracing__mutmut_39": x_setup_opentelemetry_tracing__mutmut_39,
    "x_setup_opentelemetry_tracing__mutmut_40": x_setup_opentelemetry_tracing__mutmut_40,
    "x_setup_opentelemetry_tracing__mutmut_41": x_setup_opentelemetry_tracing__mutmut_41,
    "x_setup_opentelemetry_tracing__mutmut_42": x_setup_opentelemetry_tracing__mutmut_42,
    "x_setup_opentelemetry_tracing__mutmut_43": x_setup_opentelemetry_tracing__mutmut_43,
    "x_setup_opentelemetry_tracing__mutmut_44": x_setup_opentelemetry_tracing__mutmut_44,
    "x_setup_opentelemetry_tracing__mutmut_45": x_setup_opentelemetry_tracing__mutmut_45,
    "x_setup_opentelemetry_tracing__mutmut_46": x_setup_opentelemetry_tracing__mutmut_46,
    "x_setup_opentelemetry_tracing__mutmut_47": x_setup_opentelemetry_tracing__mutmut_47,
    "x_setup_opentelemetry_tracing__mutmut_48": x_setup_opentelemetry_tracing__mutmut_48,
    "x_setup_opentelemetry_tracing__mutmut_49": x_setup_opentelemetry_tracing__mutmut_49,
    "x_setup_opentelemetry_tracing__mutmut_50": x_setup_opentelemetry_tracing__mutmut_50,
    "x_setup_opentelemetry_tracing__mutmut_51": x_setup_opentelemetry_tracing__mutmut_51,
    "x_setup_opentelemetry_tracing__mutmut_52": x_setup_opentelemetry_tracing__mutmut_52,
    "x_setup_opentelemetry_tracing__mutmut_53": x_setup_opentelemetry_tracing__mutmut_53,
    "x_setup_opentelemetry_tracing__mutmut_54": x_setup_opentelemetry_tracing__mutmut_54,
    "x_setup_opentelemetry_tracing__mutmut_55": x_setup_opentelemetry_tracing__mutmut_55,
    "x_setup_opentelemetry_tracing__mutmut_56": x_setup_opentelemetry_tracing__mutmut_56,
    "x_setup_opentelemetry_tracing__mutmut_57": x_setup_opentelemetry_tracing__mutmut_57,
    "x_setup_opentelemetry_tracing__mutmut_58": x_setup_opentelemetry_tracing__mutmut_58,
    "x_setup_opentelemetry_tracing__mutmut_59": x_setup_opentelemetry_tracing__mutmut_59,
    "x_setup_opentelemetry_tracing__mutmut_60": x_setup_opentelemetry_tracing__mutmut_60,
    "x_setup_opentelemetry_tracing__mutmut_61": x_setup_opentelemetry_tracing__mutmut_61,
    "x_setup_opentelemetry_tracing__mutmut_62": x_setup_opentelemetry_tracing__mutmut_62,
    "x_setup_opentelemetry_tracing__mutmut_63": x_setup_opentelemetry_tracing__mutmut_63,
    "x_setup_opentelemetry_tracing__mutmut_64": x_setup_opentelemetry_tracing__mutmut_64,
    "x_setup_opentelemetry_tracing__mutmut_65": x_setup_opentelemetry_tracing__mutmut_65,
    "x_setup_opentelemetry_tracing__mutmut_66": x_setup_opentelemetry_tracing__mutmut_66,
    "x_setup_opentelemetry_tracing__mutmut_67": x_setup_opentelemetry_tracing__mutmut_67,
    "x_setup_opentelemetry_tracing__mutmut_68": x_setup_opentelemetry_tracing__mutmut_68,
    "x_setup_opentelemetry_tracing__mutmut_69": x_setup_opentelemetry_tracing__mutmut_69,
    "x_setup_opentelemetry_tracing__mutmut_70": x_setup_opentelemetry_tracing__mutmut_70,
    "x_setup_opentelemetry_tracing__mutmut_71": x_setup_opentelemetry_tracing__mutmut_71,
    "x_setup_opentelemetry_tracing__mutmut_72": x_setup_opentelemetry_tracing__mutmut_72,
    "x_setup_opentelemetry_tracing__mutmut_73": x_setup_opentelemetry_tracing__mutmut_73,
    "x_setup_opentelemetry_tracing__mutmut_74": x_setup_opentelemetry_tracing__mutmut_74,
    "x_setup_opentelemetry_tracing__mutmut_75": x_setup_opentelemetry_tracing__mutmut_75,
    "x_setup_opentelemetry_tracing__mutmut_76": x_setup_opentelemetry_tracing__mutmut_76,
    "x_setup_opentelemetry_tracing__mutmut_77": x_setup_opentelemetry_tracing__mutmut_77,
    "x_setup_opentelemetry_tracing__mutmut_78": x_setup_opentelemetry_tracing__mutmut_78,
    "x_setup_opentelemetry_tracing__mutmut_79": x_setup_opentelemetry_tracing__mutmut_79,
    "x_setup_opentelemetry_tracing__mutmut_80": x_setup_opentelemetry_tracing__mutmut_80,
    "x_setup_opentelemetry_tracing__mutmut_81": x_setup_opentelemetry_tracing__mutmut_81,
    "x_setup_opentelemetry_tracing__mutmut_82": x_setup_opentelemetry_tracing__mutmut_82,
    "x_setup_opentelemetry_tracing__mutmut_83": x_setup_opentelemetry_tracing__mutmut_83,
}


def setup_opentelemetry_tracing(*args, **kwargs):
    result = _mutmut_trampoline(
        x_setup_opentelemetry_tracing__mutmut_orig, x_setup_opentelemetry_tracing__mutmut_mutants, args, kwargs
    )
    return result


setup_opentelemetry_tracing.__signature__ = _mutmut_signature(x_setup_opentelemetry_tracing__mutmut_orig)
x_setup_opentelemetry_tracing__mutmut_orig.__name__ = "x_setup_opentelemetry_tracing"


def x_get_otel_tracer__mutmut_orig(name: str) -> otel_trace.Tracer | None:
    """Get OpenTelemetry tracer if available.

    Args:
        name: Name for the tracer

    Returns:
        OpenTelemetry tracer or None if not available

    """
    if not _HAS_OTEL:
        return None

    try:
        return otel_trace.get_tracer(name)
    except Exception:
        # Broad catch intentional: OTEL tracing is optional, return None on any failure
        return None


def x_get_otel_tracer__mutmut_1(name: str) -> otel_trace.Tracer | None:
    """Get OpenTelemetry tracer if available.

    Args:
        name: Name for the tracer

    Returns:
        OpenTelemetry tracer or None if not available

    """
    if _HAS_OTEL:
        return None

    try:
        return otel_trace.get_tracer(name)
    except Exception:
        # Broad catch intentional: OTEL tracing is optional, return None on any failure
        return None


def x_get_otel_tracer__mutmut_2(name: str) -> otel_trace.Tracer | None:
    """Get OpenTelemetry tracer if available.

    Args:
        name: Name for the tracer

    Returns:
        OpenTelemetry tracer or None if not available

    """
    if not _HAS_OTEL:
        return None

    try:
        return otel_trace.get_tracer(None)
    except Exception:
        # Broad catch intentional: OTEL tracing is optional, return None on any failure
        return None


x_get_otel_tracer__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_otel_tracer__mutmut_1": x_get_otel_tracer__mutmut_1,
    "x_get_otel_tracer__mutmut_2": x_get_otel_tracer__mutmut_2,
}


def get_otel_tracer(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_otel_tracer__mutmut_orig, x_get_otel_tracer__mutmut_mutants, args, kwargs
    )
    return result


get_otel_tracer.__signature__ = _mutmut_signature(x_get_otel_tracer__mutmut_orig)
x_get_otel_tracer__mutmut_orig.__name__ = "x_get_otel_tracer"


def x_shutdown_opentelemetry__mutmut_orig() -> None:
    """Shutdown OpenTelemetry tracing."""
    if not _HAS_OTEL:
        return

    try:
        tracer_provider = otel_trace.get_tracer_provider()
        if hasattr(tracer_provider, "shutdown"):
            tracer_provider.shutdown()
            slog.debug("🔍🛑 OpenTelemetry tracer provider shutdown")
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry: {e}")


def x_shutdown_opentelemetry__mutmut_1() -> None:
    """Shutdown OpenTelemetry tracing."""
    if _HAS_OTEL:
        return

    try:
        tracer_provider = otel_trace.get_tracer_provider()
        if hasattr(tracer_provider, "shutdown"):
            tracer_provider.shutdown()
            slog.debug("🔍🛑 OpenTelemetry tracer provider shutdown")
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry: {e}")


def x_shutdown_opentelemetry__mutmut_2() -> None:
    """Shutdown OpenTelemetry tracing."""
    if not _HAS_OTEL:
        return

    try:
        tracer_provider = None
        if hasattr(tracer_provider, "shutdown"):
            tracer_provider.shutdown()
            slog.debug("🔍🛑 OpenTelemetry tracer provider shutdown")
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry: {e}")


def x_shutdown_opentelemetry__mutmut_3() -> None:
    """Shutdown OpenTelemetry tracing."""
    if not _HAS_OTEL:
        return

    try:
        tracer_provider = otel_trace.get_tracer_provider()
        if hasattr(None, "shutdown"):
            tracer_provider.shutdown()
            slog.debug("🔍🛑 OpenTelemetry tracer provider shutdown")
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry: {e}")


def x_shutdown_opentelemetry__mutmut_4() -> None:
    """Shutdown OpenTelemetry tracing."""
    if not _HAS_OTEL:
        return

    try:
        tracer_provider = otel_trace.get_tracer_provider()
        if hasattr(tracer_provider, None):
            tracer_provider.shutdown()
            slog.debug("🔍🛑 OpenTelemetry tracer provider shutdown")
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry: {e}")


def x_shutdown_opentelemetry__mutmut_5() -> None:
    """Shutdown OpenTelemetry tracing."""
    if not _HAS_OTEL:
        return

    try:
        tracer_provider = otel_trace.get_tracer_provider()
        if hasattr("shutdown"):
            tracer_provider.shutdown()
            slog.debug("🔍🛑 OpenTelemetry tracer provider shutdown")
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry: {e}")


def x_shutdown_opentelemetry__mutmut_6() -> None:
    """Shutdown OpenTelemetry tracing."""
    if not _HAS_OTEL:
        return

    try:
        tracer_provider = otel_trace.get_tracer_provider()
        if hasattr(
            tracer_provider,
        ):
            tracer_provider.shutdown()
            slog.debug("🔍🛑 OpenTelemetry tracer provider shutdown")
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry: {e}")


def x_shutdown_opentelemetry__mutmut_7() -> None:
    """Shutdown OpenTelemetry tracing."""
    if not _HAS_OTEL:
        return

    try:
        tracer_provider = otel_trace.get_tracer_provider()
        if hasattr(tracer_provider, "XXshutdownXX"):
            tracer_provider.shutdown()
            slog.debug("🔍🛑 OpenTelemetry tracer provider shutdown")
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry: {e}")


def x_shutdown_opentelemetry__mutmut_8() -> None:
    """Shutdown OpenTelemetry tracing."""
    if not _HAS_OTEL:
        return

    try:
        tracer_provider = otel_trace.get_tracer_provider()
        if hasattr(tracer_provider, "SHUTDOWN"):
            tracer_provider.shutdown()
            slog.debug("🔍🛑 OpenTelemetry tracer provider shutdown")
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry: {e}")


def x_shutdown_opentelemetry__mutmut_9() -> None:
    """Shutdown OpenTelemetry tracing."""
    if not _HAS_OTEL:
        return

    try:
        tracer_provider = otel_trace.get_tracer_provider()
        if hasattr(tracer_provider, "shutdown"):
            tracer_provider.shutdown()
            slog.debug(None)
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry: {e}")


def x_shutdown_opentelemetry__mutmut_10() -> None:
    """Shutdown OpenTelemetry tracing."""
    if not _HAS_OTEL:
        return

    try:
        tracer_provider = otel_trace.get_tracer_provider()
        if hasattr(tracer_provider, "shutdown"):
            tracer_provider.shutdown()
            slog.debug("XX🔍🛑 OpenTelemetry tracer provider shutdownXX")
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry: {e}")


def x_shutdown_opentelemetry__mutmut_11() -> None:
    """Shutdown OpenTelemetry tracing."""
    if not _HAS_OTEL:
        return

    try:
        tracer_provider = otel_trace.get_tracer_provider()
        if hasattr(tracer_provider, "shutdown"):
            tracer_provider.shutdown()
            slog.debug("🔍🛑 opentelemetry tracer provider shutdown")
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry: {e}")


def x_shutdown_opentelemetry__mutmut_12() -> None:
    """Shutdown OpenTelemetry tracing."""
    if not _HAS_OTEL:
        return

    try:
        tracer_provider = otel_trace.get_tracer_provider()
        if hasattr(tracer_provider, "shutdown"):
            tracer_provider.shutdown()
            slog.debug("🔍🛑 OPENTELEMETRY TRACER PROVIDER SHUTDOWN")
    except Exception as e:
        slog.warning(f"⚠️ Error shutting down OpenTelemetry: {e}")


def x_shutdown_opentelemetry__mutmut_13() -> None:
    """Shutdown OpenTelemetry tracing."""
    if not _HAS_OTEL:
        return

    try:
        tracer_provider = otel_trace.get_tracer_provider()
        if hasattr(tracer_provider, "shutdown"):
            tracer_provider.shutdown()
            slog.debug("🔍🛑 OpenTelemetry tracer provider shutdown")
    except Exception as e:
        slog.warning(None)


x_shutdown_opentelemetry__mutmut_mutants: ClassVar[MutantDict] = {
    "x_shutdown_opentelemetry__mutmut_1": x_shutdown_opentelemetry__mutmut_1,
    "x_shutdown_opentelemetry__mutmut_2": x_shutdown_opentelemetry__mutmut_2,
    "x_shutdown_opentelemetry__mutmut_3": x_shutdown_opentelemetry__mutmut_3,
    "x_shutdown_opentelemetry__mutmut_4": x_shutdown_opentelemetry__mutmut_4,
    "x_shutdown_opentelemetry__mutmut_5": x_shutdown_opentelemetry__mutmut_5,
    "x_shutdown_opentelemetry__mutmut_6": x_shutdown_opentelemetry__mutmut_6,
    "x_shutdown_opentelemetry__mutmut_7": x_shutdown_opentelemetry__mutmut_7,
    "x_shutdown_opentelemetry__mutmut_8": x_shutdown_opentelemetry__mutmut_8,
    "x_shutdown_opentelemetry__mutmut_9": x_shutdown_opentelemetry__mutmut_9,
    "x_shutdown_opentelemetry__mutmut_10": x_shutdown_opentelemetry__mutmut_10,
    "x_shutdown_opentelemetry__mutmut_11": x_shutdown_opentelemetry__mutmut_11,
    "x_shutdown_opentelemetry__mutmut_12": x_shutdown_opentelemetry__mutmut_12,
    "x_shutdown_opentelemetry__mutmut_13": x_shutdown_opentelemetry__mutmut_13,
}


def shutdown_opentelemetry(*args, **kwargs):
    result = _mutmut_trampoline(
        x_shutdown_opentelemetry__mutmut_orig, x_shutdown_opentelemetry__mutmut_mutants, args, kwargs
    )
    return result


shutdown_opentelemetry.__signature__ = _mutmut_signature(x_shutdown_opentelemetry__mutmut_orig)
x_shutdown_opentelemetry__mutmut_orig.__name__ = "x_shutdown_opentelemetry"


# <3 🧱🤝👣🪄
