"""OpenTelemetry integration for Foundation tracer."""

from provide.foundation.logger.config.telemetry import TelemetryConfig
from provide.foundation.logger.setup import get_vanilla_logger

slog = get_vanilla_logger(__name__)

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
    otel_trace = None
    TracerProvider = None
    BatchSpanProcessor = None
    Resource = None
    OTLPGrpcSpanExporter = None
    OTLPHttpSpanExporter = None
    TraceIdRatioBased = None


def _require_otel() -> None:
    """Ensure OpenTelemetry is available."""
    if not _HAS_OTEL:
        raise ImportError(
            "OpenTelemetry features require optional dependencies. "
            "Install with: pip install 'provide-foundation[opentelemetry]'"
        )


def setup_opentelemetry_tracing(config: TelemetryConfig) -> None:
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
            exporter = OTLPGrpcSpanExporter(
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

    # Set the global tracer provider
    otel_trace.set_tracer_provider(tracer_provider)

    slog.info("🔍✅ OpenTelemetry tracing setup complete")


def get_otel_tracer(name: str) -> "otel_trace.Tracer | None":
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
        return None


def shutdown_opentelemetry() -> None:
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
