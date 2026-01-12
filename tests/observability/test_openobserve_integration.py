#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Integration test for OpenObserve that generates and queries logs."""

from __future__ import annotations

from datetime import datetime, timedelta
import json
import os
import random
import time

from provide.testkit import FoundationTestCase
import pytest
import requests

# Skip tests if OpenObserve is not available
pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        not os.getenv("OPENOBSERVE_URL"),
        reason="OpenObserve not configured (set OPENOBSERVE_URL)",
    ),
]


class TestOpenObserveIntegration(FoundationTestCase):
    """Integration tests for OpenObserve."""

    @classmethod
    def setup_class(cls) -> None:
        """Set up test environment."""
        # Get URL and strip /api/{org} suffix if present (for compatibility)
        base_url = os.getenv("OPENOBSERVE_URL", "http://localhost:5080")
        # Remove /api/{org} suffix if present
        if "/api/" in base_url:
            base_url = base_url.split("/api/")[0]
        cls.base_url = base_url
        cls.org = os.getenv("OPENOBSERVE_ORG", "default")

        # Use credentials from environment variables
        cls.user = os.getenv("OPENOBSERVE_USER", "tim@provide.io")
        cls.password = os.getenv("OPENOBSERVE_PASSWORD", "password")

        # Create Basic Auth header from credentials
        import base64

        credentials = f"{cls.user}:{cls.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        cls.auth_header = f"Basic {encoded_credentials}"

        cls.test_stream = f"test_stream_{int(time.time())}"

    def generate_bulk_logs(self, count: int = 1000) -> str:
        """Generate bulk log data for testing.

        Args:
            count: Number of log entries to generate

        Returns:
            NDJSON formatted bulk data

        """
        logs = []
        base_time = datetime.now()

        # Log templates for realistic data
        services = [
            "api-gateway",
            "auth-service",
            "payment-service",
            "user-service",
            "notification-service",
        ]
        operations = [
            "handle_request",
            "process_payment",
            "authenticate_user",
            "send_email",
            "validate_token",
        ]
        levels = ["ERROR"] * 10 + ["WARN"] * 20 + ["INFO"] * 40 + ["DEBUG"] * 30  # Weighted distribution
        status_codes = [200, 201, 204, 400, 401, 403, 404, 500, 502, 503]
        errors = [
            "Connection timeout",
            "Database connection failed",
            "Invalid authentication token",
            "Resource not found",
            "Rate limit exceeded",
            "Internal server error",
            "Service unavailable",
        ]
        users = [f"user_{i}" for i in range(1, 101)]
        hosts = [f"host-{i}.example.com" for i in range(1, 11)]

        # Generate logs with realistic patterns
        for i in range(count):
            # Spread timestamps over last 5 minutes for better distribution
            offset_seconds = random.uniform(0, 300)
            timestamp = base_time - timedelta(seconds=offset_seconds)
            timestamp_us = int(timestamp.timestamp() * 1_000_000)

            level = random.choice(levels)
            service = random.choice(services)
            operation = random.choice(operations)
            duration_ms = random.randint(5, 5000) if level != "ERROR" else random.randint(1000, 30000)
            user = random.choice(users)
            host = random.choice(hosts)

            # Create log entry
            log_entry = {
                "_timestamp": timestamp_us,
                "level": level,
                "service": service,
                "operation": operation,
                "message": f"{operation} completed",
                "duration_ms": duration_ms,
                "user_id": user,
                "request_id": f"req_{i:010d}",
                "trace_id": f"trace_{i // 10:06d}",  # Group 10 logs per trace
                "span_id": f"span_{i:08d}",
                "host": host,
                "environment": "test",
                "version": "1.0.0",
                "status_code": random.choice(status_codes) if level == "ERROR" else 200,
            }

            # Add error details for ERROR level
            if level == "ERROR":
                log_entry["error"] = random.choice(errors)
                log_entry["stack_trace"] = f"Error at {service}.{operation}:line:{random.randint(1, 500)}"
                log_entry["message"] = f"{operation} failed: {log_entry['error']}"

            # Add additional context randomly
            if random.random() > 0.7:
                log_entry["method"] = random.choice(["GET", "POST", "PUT", "DELETE"])
                log_entry["path"] = f"/api/v1/{service.replace('-service', '')}/{operation}"

            if random.random() > 0.8:
                log_entry["client_ip"] = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
                log_entry["user_agent"] = "Mozilla/5.0 (test)"

            # Format as bulk request
            logs.append(json.dumps({"index": {"_index": self.test_stream}}))
            logs.append(json.dumps(log_entry))

        return "\n".join(logs) + "\n"

    @pytest.mark.slow
    async def test_bulk_ingestion_and_query(self) -> None:
        """Test ingesting 1000 logs and querying them."""
        # Generate logs
        print("\n📝 Generating 1000 log entries...")
        bulk_data = self.generate_bulk_logs(1000)

        # Send bulk request
        print(f"📤 Sending logs to OpenObserve stream '{self.test_stream}'...")
        start_time = time.time()

        response = requests.post(
            f"{self.base_url}/api/{self.org}/_bulk",
            headers={
                "Authorization": self.auth_header,
                "Content-Type": "application/json",
            },
            data=bulk_data,
        )

        time.time() - start_time
        assert response.status_code == 200, f"Bulk ingestion failed: {response.text}"

        result = response.json()
        assert not result.get("errors", True), f"Ingestion had errors: {result}"

        print(f"   - Items: {len(result.get('items', []))}")
        print(f"   - Took: {result.get('took', 0)}ms")

        # Wait a moment for indexing
        time.sleep(2)

        # Now query the data
        print("\n🔍 Querying ingested logs...")
        from provide.foundation.integrations.openobserve import (
            OpenObserveClient,
            search_logs,
        )

        # Set up client
        os.environ["OPENOBSERVE_URL"] = self.base_url
        os.environ["OPENOBSERVE_USER"] = "tim@provide.io"
        os.environ["OPENOBSERVE_PASSWORD"] = "password"
        os.environ["OPENOBSERVE_ORG"] = self.org

        client = OpenObserveClient.from_config()

        # Test 1: Count all logs
        response = await search_logs(
            sql=f"SELECT COUNT(*) as count FROM {self.test_stream}",
            start_time="-10m",
            client=client,
        )

        if response.hits:
            count = response.hits[0].get("count", 0)
            assert count >= 900, f"Expected at least 900 logs, got {count}"

        # Test 2: Get error logs
        response = await search_logs(
            sql=f"SELECT * FROM {self.test_stream} WHERE level = 'ERROR' LIMIT 10",
            start_time="-10m",
            client=client,
        )

        # Test 3: Aggregate by level
        response = await search_logs(
            sql=f"SELECT level, COUNT(*) as count FROM {self.test_stream} GROUP BY level",
            start_time="-10m",
            client=client,
        )

        print("\n📊 Log level distribution:")
        for hit in response.hits:
            level = hit.get("level", "UNKNOWN")
            count = hit.get("count", 0)
            print(f"   - {level}: {count}")

        # Test 4: Query by trace ID
        response = await search_logs(
            sql=f"SELECT trace_id, COUNT(*) as count FROM {self.test_stream} GROUP BY trace_id LIMIT 5",
            start_time="-10m",
            client=client,
        )

        if response.hits:
            sample_trace = response.hits[0].get("trace_id")
            if sample_trace:
                await search_logs(
                    sql=f"SELECT * FROM {self.test_stream} WHERE trace_id = '{sample_trace}'",
                    start_time="-10m",
                    client=client,
                )
                print()

        # Test 5: Performance metrics
        response = await search_logs(
            sql=f"SELECT AVG(duration_ms) as avg_duration, MAX(duration_ms) as max_duration, MIN(duration_ms) as min_duration FROM {self.test_stream}",
            start_time="-10m",
            client=client,
        )

        if response.hits:
            metrics = response.hits[0]
            print("\n⚡ Performance metrics:")
            print(f"   - Avg duration: {metrics.get('avg_duration', 0):.2f}ms")
            print(f"   - Max duration: {metrics.get('max_duration', 0)}ms")
            print(f"   - Min duration: {metrics.get('min_duration', 0)}ms")

    def test_rapid_ingestion(self) -> None:
        """Test rapid ingestion of logs in batches."""
        print("\n🚀 Testing rapid batch ingestion...")

        total_logs = 0
        start_time = time.time()

        # Send 10 batches of 100 logs each rapidly
        for batch in range(10):
            bulk_data = self.generate_bulk_logs(100)

            response = requests.post(
                f"{self.base_url}/api/{self.org}/_bulk",
                headers={
                    "Authorization": self.auth_header,
                    "Content-Type": "application/json",
                },
                data=bulk_data,
            )

            assert response.status_code == 200
            result = response.json()
            total_logs += len(result.get("items", []))

            print(
                f"   Batch {batch + 1}/10: {len(result.get('items', []))} logs in {result.get('took', 0)}ms",
            )

        elapsed = time.time() - start_time
        rate = total_logs / elapsed

        print(f"   - Total logs: {total_logs}")
        print(f"   - Time: {elapsed:.2f}s")
        print(f"   - Rate: {rate:.0f} logs/second")

        assert total_logs == 1000, f"Expected 1000 logs, got {total_logs}"
        assert elapsed < 10, f"Ingestion took too long: {elapsed}s"


if __name__ == "__main__":
    # Run directly for testing
    test = TestOpenObserveIntegration()
    test.setup_class()

    print("=" * 60)
    print("OpenObserve Integration Test")
    print("=" * 60)

    try:
        test.test_bulk_ingestion_and_query()
        test.test_rapid_ingestion()
        print("\n" + "=" * 60)
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback

        traceback.print_exc()
        exit(1)

# 🧱🏗️🔚
