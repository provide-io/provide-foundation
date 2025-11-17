#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""OpenObserve Integration Example

This example demonstrates the complete OpenObserve integration workflow:
1. Generates test logs using Foundation's logger
2. Sends them to OpenObserve via OTLP or bulk API
3. Queries them back using Foundation's OpenObserve client
4. Displays results using various formatters

Requirements:
    - OpenObserve running at http://localhost:5080
    - Environment variables:
        OPENOBSERVE_URL=http://localhost:5080/api/default
        OPENOBSERVE_USER=your_email@example.com
        OPENOBSERVE_PASSWORD=your_password
        OPENOBSERVE_ORG=default (optional)
        OPENOBSERVE_STREAM=default (optional)

Usage:
    # Start OpenObserve first (see README.md for Docker instructions)
    export OPENOBSERVE_URL=http://localhost:5080/api/default
    export OPENOBSERVE_USER=root@example.com
    export OPENOBSERVE_PASSWORD=password

    python examples/openobserve/01_openobserve_integration.py"""

from __future__ import annotations

import asyncio
from datetime import datetime
from pathlib import Path
import sys

# Add src to path for examples
example_file = Path(__file__).resolve()
project_root = example_file.parent.parent.parent
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from provide.foundation import get_hub
from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.config import OpenObserveConfig
from provide.foundation.integrations.openobserve.formatters import (
    format_json as format_json_response,
    format_output,
    format_summary,
    format_table,
)
from provide.foundation.integrations.openobserve.search import (
    aggregate_by_level,
    search_by_level,
    search_errors,
    search_logs,
)


def send_log_to_openobserve(
    client: OpenObserveClient,
    stream: str,
    message: str,
    level: str = "INFO",
    **attributes: str | int | float,
) -> bool:
    """Send a log entry to OpenObserve using the _json endpoint.

    Args:
        client: OpenObserve client
        stream: Stream name
        message: Log message
        level: Log level
        **attributes: Additional log attributes

    Returns:
        True if successful

    """
    try:
        # Build log entry with current timestamp
        log_entry = {
            "_timestamp": int(datetime.now().timestamp() * 1_000_000),
            "level": level.upper(),
            "message": message,
            **attributes,
        }

        # Send to OpenObserve _json endpoint
        endpoint = f"{stream}/_json"
        response = client._make_request(
            method="POST",
            endpoint=endpoint,
            json_data=[log_entry],
        )

        return response.get("code") == 200
    except Exception as e:
        print(f"Failed to send log: {e}")
        return False


def generate_test_logs(client: OpenObserveClient, stream: str) -> int:
    """Generate varied test logs and send them to OpenObserve.

    Args:
        client: OpenObserve client
        stream: Stream name

    Returns:
        Number of logs successfully sent

    """
    logs_sent = 0

    # Test log 1: Debug message
    if send_log_to_openobserve(
        client=client,
        stream=stream,
        message="Debug message for testing",
        level="DEBUG",
        domain="demo",
        action="debug",
        component="test_logger",
    ):
        logs_sent += 1

    # Test log 2: API request processing
    if send_log_to_openobserve(
        client=client,
        stream=stream,
        message="Processing user request",
        level="INFO",
        service="api",
        domain="api",
        action="process",
        user_id="user_123",
        endpoint="/api/users",
    ):
        logs_sent += 1

    # Test log 3: Rate limit warning
    if send_log_to_openobserve(
        client=client,
        stream=stream,
        message="Rate limit approaching",
        level="WARNING",
        service="api",
        domain="api",
        action="check",
        current_rate=95,
        limit=100,
    ):
        logs_sent += 1

    # Test log 4: Database error
    if send_log_to_openobserve(
        client=client,
        stream=stream,
        message="Database connection failed",
        level="ERROR",
        service="database",
        domain="database",
        action="connect",
        error_code="CONN_TIMEOUT",
        retry_count=3,
    ):
        logs_sent += 1

    # Test log 5: Auth success
    if send_log_to_openobserve(
        client=client,
        stream=stream,
        message="User authentication successful",
        level="INFO",
        service="auth",
        domain="auth",
        action="login",
        user_id="user_456",
        method="oauth",
    ):
        logs_sent += 1

    # Test log 6: Cache hit
    if send_log_to_openobserve(
        client=client,
        stream=stream,
        message="Cache hit",
        level="INFO",
        service="cache",
        domain="cache",
        action="get",
        key="user:123",
        ttl=3600,
    ):
        logs_sent += 1

    # Test log 7: Payment error
    if send_log_to_openobserve(
        client=client,
        stream=stream,
        message="Payment processing failed",
        level="ERROR",
        service="payment",
        domain="payment",
        action="charge",
        amount=99.99,
        currency="USD",
        error="CARD_DECLINED",
    ):
        logs_sent += 1

    # Test log 8: Email notification
    if send_log_to_openobserve(
        client=client,
        stream=stream,
        message="Email sent successfully",
        level="INFO",
        service="notification",
        domain="notification",
        action="send",
        recipient="user@example.com",
        template="welcome",
    ):
        logs_sent += 1

    return logs_sent


async def query_logs() -> None:
    """Query the generated logs from OpenObserve."""
    # Wait for logs to be indexed
    print("\n⏳ Waiting 5 seconds for logs to be indexed in OpenObserve...")
    await asyncio.sleep(5)

    # Load config and create client
    config = OpenObserveConfig.from_env()
    client = OpenObserveClient.from_config()

    stream = config.stream or "default"

    print(f"\n🔍 Querying OpenObserve stream: {stream}")
    print(f"📡 URL: {config.url}")
    print(f"👤 User: {config.user}")

    # Test connection
    if not client.test_connection():
        print("❌ Failed to connect to OpenObserve")
        return

    # Query 1: Get all recent logs
    print("=" * 80)
    print("Query 1: All recent logs from last 10 minutes")
    print("=" * 80)

    sql = f"SELECT * FROM {stream}"
    response = search_logs(
        sql=sql,
        start_time="-10m",
        end_time="now",
        size=20,
        client=client,
    )

    print(f"Total hits: {response.total}")
    print(f"Query took: {response.took}ms")
    print(f"Scan size: {response.scan_size} bytes\n")

    if response.hits:
        print("📋 Log Format:")
        print(format_output(response, format_type="log"))

        print("\n📊 Table Format:")
        print(format_table(response))
    else:
        print("⚠️  No logs found in last 10 minutes")

    # Query 2: Search for errors only
    print("\n" + "=" * 80)
    print("Query 2: Error logs only")
    print("=" * 80)

    errors = search_errors(
        stream=stream,
        start_time="-10m",
        client=client,
    )

    print(f"Total errors: {errors.total}\n")

    if errors.hits:
        print(format_output(errors, format_type="log"))
    else:
        print("⚠️  No errors found in last 10 minutes")

    # Query 3: Search by specific domain
    print("\n" + "=" * 80)
    print("Query 3: API domain logs")
    print("=" * 80)

    api_sql = f"SELECT * FROM {stream} WHERE domain = 'api'"
    api_logs = search_logs(
        sql=api_sql,
        start_time="-10m",
        client=client,
    )

    print(f"API logs found: {api_logs.total}\n")

    if api_logs.hits:
        print(format_output(api_logs, format_type="log"))

    # Query 4: Aggregate by log level
    print("\n" + "=" * 80)
    print("Query 4: Aggregate counts by log level")
    print("=" * 80)

    aggregation = aggregate_by_level(
        stream=stream,
        start_time="-10m",
        client=client,
    )

    print("\n📊 Log Level Distribution:")
    for level, count in sorted(aggregation.items()):
        print(f"  {level}: {count}")

    # Query 5: Search by log level
    print("\n" + "=" * 80)
    print("Query 5: INFO level logs")
    print("=" * 80)

    info_logs = search_by_level(
        level="INFO",
        stream=stream,
        start_time="-10m",
        size=10,
        client=client,
    )

    print(f"INFO logs found: {info_logs.total}\n")

    if info_logs.hits:
        print("📝 Summary Format:")
        print(format_summary(info_logs))

    # Query 6: Get raw JSON response
    print("\n" + "=" * 80)
    print("Query 6: JSON format output")
    print("=" * 80)

    recent_sql = f"SELECT * FROM {stream} LIMIT 3"
    recent = search_logs(
        sql=recent_sql,
        start_time="-10m",
        client=client,
    )

    if recent.hits:
        print(format_json_response(recent, pretty=True))


async def main() -> None:
    """Main execution function."""
    print("🚀 OpenObserve Integration Demo")
    print("=" * 80)

    # Initialize Foundation
    hub = get_hub()
    hub.initialize_foundation()

    # Create OpenObserve client
    print("\n📡 Connecting to OpenObserve...")
    config = OpenObserveConfig.from_env()
    client = OpenObserveClient.from_config()

    if not client.test_connection():
        print("❌ Failed to connect to OpenObserve")
        print("   Please ensure OpenObserve is running and credentials are correct")
        return

    stream = config.stream or "default"
    print(f"   Organization: {config.org or 'default'}")
    print(f"   Stream: {stream}")

    # Generate and send test logs
    print("\n📝 Generating and sending test logs...")
    generate_test_logs(client, stream)

    # Query the logs
    await query_logs()

    print("\n" + "=" * 80)
    print("✨ Demo complete!")
    print("\nTo view logs in OpenObserve UI:")
    print("  1. Open http://localhost:5080")
    print("  2. Login with your credentials")
    print("  3. Navigate to Logs section")
    print(f"  4. Select the '{stream}' stream")


if __name__ == "__main__":
    asyncio.run(main())

# 🧱🏗️🔚
