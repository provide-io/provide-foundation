"""Demonstrate OpenObserve integration with Foundation.

This script:
1. Generates test logs using Foundation's logger
2. Sends them to OpenObserve via OTLP
3. Queries them back using Foundation's OpenObserve API
4. Displays results using various formatters

Requirements:
    - OpenObserve running at http://localhost:5080
    - Environment variables set (OPENOBSERVE_URL, OPENOBSERVE_USER, OPENOBSERVE_PASSWORD)
"""

from __future__ import annotations

import asyncio

from provide.foundation import get_hub, logger
from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.config import OpenObserveConfig
from provide.foundation.integrations.openobserve.formatters import (
    format_json,
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


def generate_test_logs() -> None:
    """Generate varied test logs to send to OpenObserve."""
    logger.info("Starting log generation", domain="demo", action="start")

    # Generate logs at different levels
    logger.debug(
        "Debug message for testing",
        domain="demo",
        action="debug",
        component="test_logger",
    )

    logger.info(
        "Processing user request",
        domain="api",
        action="process",
        user_id="user_123",
        endpoint="/api/users",
    )

    logger.warning(
        "Rate limit approaching",
        domain="api",
        action="check",
        current_rate=95,
        limit=100,
    )

    logger.error(
        "Database connection failed",
        domain="database",
        action="connect",
        error_code="CONN_TIMEOUT",
        retry_count=3,
    )

    logger.info(
        "User authentication successful",
        domain="auth",
        action="login",
        user_id="user_456",
        method="oauth",
    )

    logger.info(
        "Cache hit",
        domain="cache",
        action="get",
        key="user:123",
        ttl=3600,
    )

    logger.error(
        "Payment processing failed",
        domain="payment",
        action="charge",
        amount=99.99,
        currency="USD",
        error="CARD_DECLINED",
    )

    logger.info(
        "Email sent successfully",
        domain="notification",
        action="send",
        recipient="user@example.com",
        template="welcome",
    )

    logger.info("Log generation complete", domain="demo", action="complete", count=8)


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

    print("✅ Connected to OpenObserve successfully\n")

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
        print("✅ No errors found")

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
        print(format_json(recent, pretty=True))


async def main() -> None:
    """Main execution function."""
    print("🚀 OpenObserve Integration Demo")
    print("=" * 80)

    # Initialize Foundation with OTLP enabled
    hub = get_hub()
    hub.initialize_foundation()

    print("\n📝 Generating test logs...")
    generate_test_logs()

    print("\n✅ Logs generated and sent to OpenObserve via OTLP")

    # Query the logs
    await query_logs()

    print("\n" + "=" * 80)
    print("✨ Demo complete!")
    print("\nTo view logs in OpenObserve UI:")
    print("  1. Open http://localhost:5080")
    print("  2. Login with your credentials")
    print("  3. Navigate to Logs section")
    print("  4. Select the 'default' stream")


if __name__ == "__main__":
    asyncio.run(main())
