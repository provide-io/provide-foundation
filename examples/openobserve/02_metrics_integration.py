#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""OpenObserve Metrics Integration Example.

This example demonstrates the complete OpenObserve metrics integration workflow:
1. Initializes Foundation with OTLP metrics export enabled
2. Creates and records various metric types (counters, gauges, histograms)
3. Waits for metrics to be exported to OpenObserve
4. Queries metrics back using Foundation's OpenObserve client
5. Displays results in various formats

Requirements:
    - OpenObserve running at http://localhost:5080
    - Environment variables:
        OPENOBSERVE_URL=http://localhost:5080/api/default
        OPENOBSERVE_USER=tim@provide.io
        OPENOBSERVE_PASSWORD=password
        OPENOBSERVE_ORG=default (optional)

Usage:
    # Start OpenObserve first
    export OPENOBSERVE_URL=http://localhost:5080/api/default
    export OPENOBSERVE_USER=tim@provide.io
    export OPENOBSERVE_PASSWORD=password

    python examples/openobserve/02_metrics_integration.py"""

from __future__ import annotations

import asyncio
from pathlib import Path
import sys
import time

# Add src to path for examples
example_file = Path(__file__).resolve()
project_root = example_file.parent.parent.parent
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.config import OpenObserveConfig
from provide.foundation.integrations.openobserve.metrics_formatters import (
    format_metric_output,
)
from provide.foundation.integrations.openobserve.otlp_adapter import (
    get_openobserve_otlp_metrics_endpoint,
)
from provide.foundation.logger.config.telemetry import TelemetryConfig
from provide.foundation.metrics import counter, gauge, histogram
from provide.foundation.metrics.otel import (
    setup_opentelemetry_metrics,
    shutdown_opentelemetry_metrics,
)


def create_and_record_metrics() -> dict[str, object]:
    """Create test metrics and record values.

    Returns:
        Dictionary of created metrics
    """
    print("\n📊 Creating test metrics...")

    # Create different metric types
    request_counter = counter(
        "example_http_requests_total",
        "Total HTTP requests",
        "requests",
    )

    active_connections_gauge = gauge(
        "example_active_connections",
        "Number of active connections",
        "connections",
    )

    request_duration_histogram = histogram(
        "example_request_duration_seconds",
        "HTTP request duration",
        "seconds",
    )

    # Record some values
    print("\n📝 Recording metric values...")

    # Increment counter multiple times
    for i in range(1, 11):
        request_counter.inc(i)
    print(f"  Counter: {request_counter.name} (incremented 10 times)")

    # Set and modify gauge
    active_connections_gauge.set(50)
    active_connections_gauge.inc(25)
    active_connections_gauge.dec(10)
    print(f"  Gauge: {active_connections_gauge.name} (set to 50, +25, -10 = 65)")

    # Record histogram observations
    durations = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.5, 0.75, 1.0, 1.5]
    for duration in durations:
        request_duration_histogram.observe(duration)
    print(f"  Histogram: {request_duration_histogram.name} (10 observations)")

    return {
        "counter": request_counter,
        "gauge": active_connections_gauge,
        "histogram": request_duration_histogram,
    }


async def query_and_display_metrics(client: OpenObserveClient) -> None:
    """Query metrics from OpenObserve and display in various formats.

    Args:
        client: OpenObserve client instance
    """
    print("\n" + "=" * 80)
    print("QUERYING METRICS FROM OPENOBSERVE")
    print("=" * 80)

    # Query 1: List all available metrics
    print("\n1. Listing all metrics...")
    try:
        metrics = await client.list_metrics()
        example_metrics = [m for m in metrics if m.startswith("example_")]

        if example_metrics:
            for metric in example_metrics:
                print(f"  - {metric}")
        else:
            print("⚠️  No example metrics found yet (may still be exporting)")

    except Exception as e:
        print(f"❌ Failed to list metrics: {e}")

    # Query 2: Get metadata for our metrics
    print("\n2. Getting metric metadata...")
    try:
        for metric_name in ["example_http_requests_total", "example_active_connections"]:
            metadata = await client.get_metric_metadata(metric=metric_name)
            if metadata:
                print(f"\n  {metric_name}:")
                for meta_list in metadata.values():
                    for meta in meta_list:
                        print(f"    Type: {meta.get('type', 'unknown')}")
                        print(f"    Help: {meta.get('help', '')}")
            else:
                print(f"  {metric_name}: No metadata available")

    except Exception as e:
        print(f"❌ Failed to get metadata: {e}")

    # Query 3: Instant query for counter metric
    print("\n3. Querying counter metric (instant query)...")
    try:
        result = await client.query_promql("example_http_requests_total")

        if result.is_success and result.result:
            print(format_metric_output(result, format_type="table"))
        else:
            print(f"⚠️  No data or query failed: {result.error if not result.is_success else 'no results'}")

    except Exception as e:
        print(f"❌ Query failed: {e}")

    # Query 4: Query gauge metric
    print("\n4. Querying gauge metric...")
    try:
        result = await client.query_promql("example_active_connections")

        if result.is_success and result.result:
            print(format_metric_output(result, format_type="summary"))
        else:
            print(f"⚠️  No data or query failed: {result.error if not result.is_success else 'no results'}")

    except Exception as e:
        print(f"❌ Query failed: {e}")

    # Query 5: Range query for histogram
    print("\n5. Querying histogram metric (range query, last 5 minutes)...")
    try:
        now = int(time.time())
        start = now - 300  # 5 minutes ago

        result = await client.query_range_promql(
            query="example_request_duration_seconds",
            start=start,
            end=now,
            step="30s",
        )

        if result.is_success and result.result:
            print(f"Result type: {result.result_type}")
            print(f"Series count: {len(result.result)}")

            # Show first series details
            if result.result:
                print("\nFirst series:")
                sample = result.result[0]
                print(f"  Metric: {sample.metric}")
                print(f"  Data points: {len(sample.values)}")

        else:
            print(f"⚠️  No data or query failed: {result.error if not result.is_success else 'no results'}")

    except Exception as e:
        print(f"❌ Range query failed: {e}")

    # Query 6: Get labels
    print("\n6. Getting metric labels...")
    try:
        labels = await client.get_metric_labels("example_http_requests_total")

        if labels:
            for label in labels:
                print(f"  - {label}")
        else:
            print("⚠️  No labels found")

    except Exception as e:
        print(f"❌ Failed to get labels: {e}")


async def main() -> None:
    """Main execution function."""
    print("=" * 80)
    print("🚀 OpenObserve Metrics Integration Demo")
    print("=" * 80)

    # Check configuration
    oo_config = OpenObserveConfig.from_env()
    if not oo_config.is_configured():
        print("\n❌ OpenObserve not configured!")
        print("   Please set environment variables:")
        print("     OPENOBSERVE_URL=http://localhost:5080/api/default")
        print("     OPENOBSERVE_USER=tim@provide.io")
        print("     OPENOBSERVE_PASSWORD=password")
        return

    print(f"   URL: {oo_config.url}")
    print(f"   User: {oo_config.user}")
    print(f"   Organization: {oo_config.org or 'default'}")

    # Setup OTLP metrics export
    otlp_endpoint = get_openobserve_otlp_metrics_endpoint(oo_config.url, oo_config.org)  # type: ignore[arg-type]
    print(f"   OTLP endpoint: {otlp_endpoint}")

    telemetry_config = TelemetryConfig(
        service_name="foundation-example-metrics",
        service_version="1.0.0",
        otlp_endpoint=otlp_endpoint,
        otlp_protocol="http/protobuf",
        metrics_enabled=True,
        globally_disabled=False,
    )

    setup_opentelemetry_metrics(telemetry_config)

    # Create and record metrics
    create_and_record_metrics()

    # Force metrics export by shutting down provider
    print("\n⏳ Forcing metrics export (shutting down provider)...")
    shutdown_opentelemetry_metrics()

    # Wait for metrics to reach OpenObserve
    print("\n⏳ Waiting 5 seconds for metrics to be ingested by OpenObserve...")
    await asyncio.sleep(5)

    # Create client and query metrics
    print("\n📊 Creating OpenObserve client...")
    client = OpenObserveClient.from_config()

    # Test connection
    if not await client.test_connection():
        print("❌ Failed to connect to OpenObserve")
        return

    # Query and display metrics
    await query_and_display_metrics(client)

    # Summary
    print("\n" + "=" * 80)
    print("✨ Demo complete!")
    print("\nWhat we demonstrated:")
    print("\nTo view metrics in OpenObserve UI:")
    print("  1. Open http://localhost:5080")
    print("  2. Login with your credentials")
    print("  3. Navigate to Metrics section")
    print("  4. Search for 'example_' metrics")
    print("\nTry the CLI commands:")
    print("  foundation openobserve metrics list")
    print('  foundation openobserve metrics query "example_http_requests_total"')
    print("  foundation openobserve metrics info example_http_requests_total")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())

# 🧱🏗️🔚
