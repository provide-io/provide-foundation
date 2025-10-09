#!/bin/bash
# OpenObserve environment configuration for OTLP integration

# OpenObserve API configuration (for querying)
export OPENOBSERVE_URL=http://localhost:5080/api/default
export OPENOBSERVE_USER=tim@provide.io
export OPENOBSERVE_PASSWORD=password
export OPENOBSERVE_ORG=default
export OPENOBSERVE_STREAM=default

# OpenTelemetry OTLP configuration (for sending logs)
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:5080
export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf

# Authentication headers (Basic auth with base64 encoded credentials)
# Format: Authorization=Basic <base64(user:password)>
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Basic $(echo -n 'tim@provide.io:password' | base64),organization=default"

# Service identification
export OTEL_SERVICE_NAME=provide-foundation-demo

# Enable tracing (optional)
export OTEL_TRACING_ENABLED=true

echo "✅ OpenObserve environment variables configured"
echo "   OTLP Endpoint: $OTEL_EXPORTER_OTLP_ENDPOINT"
echo "   Service Name: $OTEL_SERVICE_NAME"
echo "   Protocol: $OTEL_EXPORTER_OTLP_PROTOCOL"
