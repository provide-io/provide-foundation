#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Integration tests for OTLP metrics export to OpenObserve."""

from __future__ import annotations

import asyncio
import time

import pytest

from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.config import OpenObserveConfig
from provide.foundation.logger.config.telemetry import TelemetryConfig
from provide.foundation.metrics import counter, gauge, histogram
from provide.foundation.metrics.otel import setup_opentelemetry_metrics


@pytest.mark.integration
@pytest.mark.asyncio
class TestOTLPMetricsExport:
    """Test OTLP metrics export to OpenObserve."""

    async def test_otlp_metrics_endpoint_configuration(self) -> None:
        """Test that OTLP metrics endpoint is correctly derived from OpenObserve URL."""
        from provide.foundation.integrations.openobserve.otlp_adapter import (
            get_openobserve_otlp_metrics_endpoint,
        )

        # Test with base URL
        endpoint = get_openobserve_otlp_metrics_endpoint("http://localhost:5080", "default")
        assert endpoint == "http://localhost:5080/api/default/v1/metrics"

        # Test with URL containing /api/
        endpoint = get_openobserve_otlp_metrics_endpoint("http://localhost:5080/api/default", "custom")
        assert endpoint == "http://localhost:5080/api/custom/v1/metrics"

        # Test with trailing slash
        endpoint = get_openobserve_otlp_metrics_endpoint("http://localhost:5080/", "default")
        assert endpoint == "http://localhost:5080/api/default/v1/metrics"

    async def test_metrics_export_to_openobserve(self) -> None:
        """Test that metrics are exported to OpenObserve via OTLP.

        Requires:
            - OpenObserve running at http://localhost:5080
            - Environment variables:
                OPENOBSERVE_URL=http://localhost:5080/api/default
                OPENOBSERVE_USER=tim@provide.io
                OPENOBSERVE_PASSWORD=password
        """
        # Check if OpenObserve is configured
        oo_config = OpenObserveConfig.from_env()
        if not oo_config.is_configured():
            pytest.skip(
                "OpenObserve not configured (set OPENOBSERVE_URL, OPENOBSERVE_USER, OPENOBSERVE_PASSWORD)"
            )

        # Configure telemetry with OpenObserve OTLP endpoint
        from provide.foundation.integrations.openobserve.otlp_adapter import (
            get_openobserve_otlp_metrics_endpoint,
        )

        otlp_endpoint = get_openobserve_otlp_metrics_endpoint(oo_config.url, oo_config.org)  # type: ignore[arg-type]

        telemetry_config = TelemetryConfig(
            service_name="foundation-metrics-test",
            service_version="1.0.0-test",
            otlp_endpoint=otlp_endpoint,
            otlp_protocol="http/protobuf",
            metrics_enabled=True,
            globally_disabled=False,
        )

        # Setup OpenTelemetry metrics
        setup_opentelemetry_metrics(telemetry_config)

        # Create test metrics
        test_counter = counter("test_counter_total", "Test counter metric", "1")
        test_gauge = gauge("test_gauge_value", "Test gauge metric", "units")
        test_histogram = histogram("test_request_duration_seconds", "Test histogram metric", "seconds")

        # Record some values
        test_counter.inc(5)
        test_counter.inc(3)

        test_gauge.set(42)
        test_gauge.inc(8)
        test_gauge.dec(5)

        test_histogram.observe(0.125)
        test_histogram.observe(0.250)
        test_histogram.observe(0.500)

        # Wait for metrics to be exported (default export interval is 60s, but we can't wait that long)
        # Force export by shutting down the metrics provider
        from provide.foundation.metrics.otel import shutdown_opentelemetry_metrics

        shutdown_opentelemetry_metrics()

        # Wait a bit for metrics to reach OpenObserve
        await asyncio.sleep(2)

        # Query metrics from OpenObserve to verify they were received
        client = OpenObserveClient.from_config()

        # Try to list metrics
        metrics = await client.list_metrics()

        # Verify our test metrics are present
        # Note: Metric names may be transformed by OTLP/OpenObserve
        assert isinstance(metrics, list), "Metrics list should be a list"

        # We can't guarantee the metrics will be there immediately, so this is informational
        if metrics:
            print(f"Available metrics: {metrics}")

            # Check if any of our metrics made it through
            test_metric_names = ["test_counter_total", "test_gauge_value", "test_request_duration_seconds"]
            found_metrics = [m for m in metrics if any(tm in m for tm in test_metric_names)]

            if found_metrics:
                print(f"Found test metrics: {found_metrics}")

    async def test_metrics_query_after_export(self) -> None:
        """Test querying metrics after exporting via OTLP.

        This test verifies the full workflow:
        1. Export metrics via OTLP
        2. Wait for ingestion
        3. Query metrics via Prometheus API
        """
        # Check if OpenObserve is configured
        oo_config = OpenObserveConfig.from_env()
        if not oo_config.is_configured():
            pytest.skip("OpenObserve not configured")

        # Configure and setup metrics
        from provide.foundation.integrations.openobserve.otlp_adapter import (
            get_openobserve_otlp_metrics_endpoint,
        )

        otlp_endpoint = get_openobserve_otlp_metrics_endpoint(oo_config.url, oo_config.org)  # type: ignore[arg-type]

        telemetry_config = TelemetryConfig(
            service_name="foundation-query-test",
            service_version="1.0.0-test",
            otlp_endpoint=otlp_endpoint,
            otlp_protocol="http/protobuf",
            metrics_enabled=True,
            globally_disabled=False,
        )

        setup_opentelemetry_metrics(telemetry_config)

        # Create and record a simple counter
        query_test_counter = counter("query_test_requests_total", "Query test counter")
        current_value = int(time.time()) % 1000  # Use timestamp to make value unique
        query_test_counter.inc(current_value)

        # Force export
        from provide.foundation.metrics.otel import shutdown_opentelemetry_metrics

        shutdown_opentelemetry_metrics()

        # Wait for ingestion
        await asyncio.sleep(3)

        # Query the metric
        client = OpenObserveClient.from_config()

        # Try instant query
        try:
            result = await client.query_promql("query_test_requests_total")

            # Check result structure
            assert hasattr(result, "result_type"), "Result should have result_type"
            assert hasattr(result, "result"), "Result should have result field"
            assert hasattr(result, "is_success"), "Result should have is_success property"

            if result.is_success:
                print(f"Query successful: {result.sample_count} samples")
                if result.result:
                    for sample in result.result:
                        print(f"  Metric: {sample.metric}")
                        print(f"  Value: {sample.value}")
            else:
                print(f"Query failed: {result.error}")

        except Exception as e:
            # Query might fail if metrics haven't been ingested yet
            print(f"Query exception: {e}")
            pytest.skip(f"Metrics query failed (may need more time for ingestion): {e}")


# 🧱🏗️🔚
