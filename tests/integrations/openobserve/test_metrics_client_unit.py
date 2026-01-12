#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for OpenObserve metrics client methods."""

from __future__ import annotations

from provide.testkit.mocking import AsyncMock, patch
import pytest

from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.metrics_models import MetricQueryResult


class TestListMetrics:
    """Tests for list_metrics method."""

    @pytest.mark.asyncio
    async def test_list_metrics_success(self) -> None:
        """Test successful metrics listing."""
        # Setup
        mock_response = {"status": "success", "data": ["metric1", "metric2", "metric3"]}

        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test",
            password="test",
        )

        # Mock the _make_request method
        with patch.object(client, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            # Execute
            result = await client.list_metrics()

            # Assert
            assert result == ["metric1", "metric2", "metric3"]
            mock_request.assert_called_once_with(
                method="GET",
                endpoint="prometheus/api/v1/label/__name__/values",
            )

    @pytest.mark.asyncio
    async def test_list_metrics_empty(self) -> None:
        """Test listing metrics when none exist."""
        mock_response = {"status": "success", "data": []}

        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test",
            password="test",
        )

        with patch.object(client, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            result = await client.list_metrics()

            assert result == []

    @pytest.mark.asyncio
    async def test_list_metrics_error_status(self) -> None:
        """Test listing metrics with error status."""
        mock_response = {"status": "error", "errorType": "bad_data", "error": "invalid query"}

        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test",
            password="test",
        )

        with patch.object(client, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            result = await client.list_metrics()

            assert result == []


class TestQueryPromQL:
    """Tests for query_promql method."""

    @pytest.mark.asyncio
    async def test_query_promql_basic(self) -> None:
        """Test basic PromQL query."""
        mock_response = {
            "status": "success",
            "data": {
                "resultType": "vector",
                "result": [{"metric": {"__name__": "up", "job": "test"}, "value": [1234567890, "1"]}],
            },
        }

        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test",
            password="test",
        )

        with patch.object(client, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            result = await client.query_promql("up")

            assert isinstance(result, MetricQueryResult)
            assert result.is_success
            assert result.result_type == "vector"
            assert len(result.result) == 1

            mock_request.assert_called_once_with(
                method="GET",
                endpoint="prometheus/api/v1/query",
                params={"query": "up"},
            )

    @pytest.mark.asyncio
    async def test_query_promql_with_time(self) -> None:
        """Test PromQL query with specific time."""
        mock_response = {
            "status": "success",
            "data": {"resultType": "vector", "result": []},
        }

        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test",
            password="test",
        )

        with patch.object(client, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            await client.query_promql("up", time=1234567890)

            mock_request.assert_called_once_with(
                method="GET",
                endpoint="prometheus/api/v1/query",
                params={"query": "up", "time": 1234567890},
            )

    @pytest.mark.asyncio
    async def test_query_promql_with_timeout(self) -> None:
        """Test PromQL query with timeout."""
        mock_response = {
            "status": "success",
            "data": {"resultType": "vector", "result": []},
        }

        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test",
            password="test",
        )

        with patch.object(client, "_make_request", new_callable=AsyncMock) as mock_request:
            AsyncMock()
            mock_request.return_value = mock_response

            await client.query_promql("up", timeout="30s")

            mock_request.assert_called_once_with(
                method="GET",
                endpoint="prometheus/api/v1/query",
                params={"query": "up", "timeout": "30s"},
            )

    @pytest.mark.asyncio
    async def test_query_promql_error(self) -> None:
        """Test PromQL query that returns error."""
        mock_response = {
            "status": "error",
            "errorType": "bad_data",
            "error": "invalid query",
        }

        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test",
            password="test",
        )

        with patch.object(client, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            result = await client.query_promql("invalid{")

            assert isinstance(result, MetricQueryResult)
            assert not result.is_success
            assert result.error == "invalid query"
            assert result.error_type == "bad_data"


class TestQueryRangePromQL:
    """Tests for query_range_promql method."""

    @pytest.mark.asyncio
    async def test_query_range_promql_basic(self) -> None:
        """Test basic PromQL range query."""
        mock_response = {
            "status": "success",
            "data": {
                "resultType": "matrix",
                "result": [
                    {
                        "metric": {"__name__": "up", "job": "test"},
                        "values": [[1234567890, "1"], [1234567900, "1"], [1234567910, "0"]],
                    }
                ],
            },
        }

        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test",
            password="test",
        )

        with patch.object(client, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            result = await client.query_range_promql(
                query="up",
                start=1234567890,
                end=1234567910,
                step=10,
            )

            assert isinstance(result, MetricQueryResult)
            assert result.is_success
            assert result.result_type == "matrix"
            assert len(result.result) == 1
            assert len(result.result[0].values) == 3

            mock_request.assert_called_once_with(
                method="GET",
                endpoint="prometheus/api/v1/query_range",
                params={"query": "up", "start": 1234567890, "end": 1234567910, "step": 10},
            )

    @pytest.mark.asyncio
    async def test_query_range_promql_with_timeout(self) -> None:
        """Test range query with timeout."""
        mock_response = {
            "status": "success",
            "data": {"resultType": "matrix", "result": []},
        }

        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test",
            password="test",
        )

        with patch.object(client, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            await client.query_range_promql(
                query="up",
                start=1234567890,
                end=1234567910,
                step="15s",
                timeout="60s",
            )

            mock_request.assert_called_once_with(
                method="GET",
                endpoint="prometheus/api/v1/query_range",
                params={
                    "query": "up",
                    "start": 1234567890,
                    "end": 1234567910,
                    "step": "15s",
                    "timeout": "60s",
                },
            )


class TestGetMetricMetadata:
    """Tests for get_metric_metadata method."""

    @pytest.mark.asyncio
    async def test_get_metric_metadata_all(self) -> None:
        """Test getting metadata for all metrics."""
        mock_response = {
            "status": "success",
            "data": {
                "http_requests_total": [{"type": "counter", "help": "Total HTTP requests", "unit": ""}],
                "process_cpu_seconds_total": [{"type": "counter", "help": "CPU time", "unit": "seconds"}],
            },
        }

        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test",
            password="test",
        )

        with patch.object(client, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            result = await client.get_metric_metadata()

            assert len(result) == 2
            assert "http_requests_total" in result
            assert result["http_requests_total"][0]["type"] == "counter"

            mock_request.assert_called_once_with(
                method="GET",
                endpoint="prometheus/api/v1/metadata",
                params={},
            )

    @pytest.mark.asyncio
    async def test_get_metric_metadata_specific(self) -> None:
        """Test getting metadata for specific metric."""
        mock_response = {
            "status": "success",
            "data": {"http_requests_total": [{"type": "counter", "help": "Total HTTP requests"}]},
        }

        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test",
            password="test",
        )

        with patch.object(client, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            result = await client.get_metric_metadata("http_requests_total")

            assert len(result) == 1
            assert "http_requests_total" in result

            mock_request.assert_called_once_with(
                method="GET",
                endpoint="prometheus/api/v1/metadata",
                params={"metric": "http_requests_total"},
            )


class TestGetMetricLabels:
    """Tests for get_metric_labels method."""

    @pytest.mark.asyncio
    async def test_get_metric_labels_all(self) -> None:
        """Test getting all label names."""
        mock_response = {"status": "success", "data": ["__name__", "job", "instance", "method"]}

        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test",
            password="test",
        )

        with patch.object(client, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            result = await client.get_metric_labels()

            assert len(result) == 4
            assert "__name__" in result
            assert "job" in result

            mock_request.assert_called_once_with(
                method="GET",
                endpoint="prometheus/api/v1/labels",
                params={},
            )

    @pytest.mark.asyncio
    async def test_get_metric_labels_for_metric(self) -> None:
        """Test getting labels for specific metric."""
        mock_response = {"status": "success", "data": ["job", "instance", "method"]}

        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test",
            password="test",
        )

        with patch.object(client, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            result = await client.get_metric_labels("http_requests_total")

            assert len(result) == 3

            mock_request.assert_called_once_with(
                method="GET",
                endpoint="prometheus/api/v1/labels",
                params={"match[]": "{http_requests_total=~'.+'}"},
            )


class TestGetLabelValues:
    """Tests for get_label_values method."""

    @pytest.mark.asyncio
    async def test_get_label_values_basic(self) -> None:
        """Test getting values for a label."""
        mock_response = {"status": "success", "data": ["api", "web", "worker"]}

        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test",
            password="test",
        )

        with patch.object(client, "_make_request", new_callable=AsyncMock) as mock_request:
            AsyncMock()
            mock_request.return_value = mock_response

            result = await client.get_label_values("job")

            assert len(result) == 3
            assert "api" in result
            assert "web" in result

            mock_request.assert_called_once_with(
                method="GET",
                endpoint="prometheus/api/v1/label/job/values",
                params={},
            )

    @pytest.mark.asyncio
    async def test_get_label_values_with_match(self) -> None:
        """Test getting label values with series selector."""
        mock_response = {"status": "success", "data": ["200", "404", "500"]}

        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test",
            password="test",
        )

        with patch.object(client, "_make_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            result = await client.get_label_values("status_code", match=["{job='api'}"])

            assert len(result) == 3

            mock_request.assert_called_once_with(
                method="GET",
                endpoint="prometheus/api/v1/label/status_code/values",
                params={"match[]": ["{job='api'}"]},
            )


# 🧱🏗️🔚
