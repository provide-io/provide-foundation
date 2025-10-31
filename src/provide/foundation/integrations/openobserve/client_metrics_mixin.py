#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Metrics and Prometheus API operations for OpenObserve client."""

from __future__ import annotations

from typing import Any

from provide.foundation.logger import get_logger

log = get_logger(__name__)


class MetricsOperationsMixin:
    """Mixin providing Prometheus-compatible metrics operations."""

    async def list_metrics(self) -> list[str]:
        """List all available metrics.

        Uses the Prometheus API endpoint to get all metric names.

        Returns:
            List of metric names

        """

        # Query for all unique metric names using __name__ label
        response = await self._make_request(
            method="GET",
            endpoint="prometheus/api/v1/label/__name__/values",
        )

        # Response format: {"status": "success", "data": ["metric1", "metric2", ...]}
        if response.get("status") == "success":
            return response.get("data", [])

        return []

    async def query_promql(
        self,
        query: str,
        time: str | int | None = None,
        timeout: str | None = None,
    ) -> Any:
        """Execute instant PromQL query.

        Args:
            query: PromQL query string
            time: Evaluation timestamp (Unix timestamp or RFC3339, defaults to now)
            timeout: Query timeout

        Returns:
            MetricQueryResult with query results

        """
        from provide.foundation.integrations.openobserve.metrics_models import (
            MetricQueryResult,
        )

        params: dict[str, Any] = {"query": query}

        if time is not None:
            params["time"] = time
        if timeout is not None:
            params["timeout"] = timeout

        log.debug(f"Executing PromQL query: {query}")

        response = await self._make_request(
            method="GET",
            endpoint="prometheus/api/v1/query",
            params=params,
        )

        result = MetricQueryResult.from_dict(response)

        if not result.is_success:
            log.warning(f"Query returned error: {result.error}")

        log.info(f"PromQL query completed: {result.sample_count} samples")

        return result

    async def query_range_promql(
        self,
        query: str,
        start: str | int,
        end: str | int,
        step: str | int,
        timeout: str | None = None,
    ) -> Any:
        """Execute PromQL range query.

        Args:
            query: PromQL query string
            start: Start timestamp (Unix timestamp or RFC3339)
            end: End timestamp (Unix timestamp or RFC3339)
            step: Query resolution step (duration string like "15s" or seconds as int)
            timeout: Query timeout

        Returns:
            MetricQueryResult with time series data

        """
        from provide.foundation.integrations.openobserve.metrics_models import (
            MetricQueryResult,
        )

        params: dict[str, Any] = {
            "query": query,
            "start": start,
            "end": end,
            "step": step,
        }

        if timeout is not None:
            params["timeout"] = timeout

        log.debug(f"Executing PromQL range query: {query} from {start} to {end}, step {step}")

        response = await self._make_request(
            method="GET",
            endpoint="prometheus/api/v1/query_range",
            params=params,
        )

        result = MetricQueryResult.from_dict(response)

        if not result.is_success:
            log.warning(f"Range query returned error: {result.error}")

        log.info(f"PromQL range query completed: {result.sample_count} series")

        return result

    async def get_metric_metadata(self, metric: str | None = None) -> dict[str, list[dict[str, Any]]]:
        """Get metadata for metrics.

        Args:
            metric: Optional metric name to filter metadata

        Returns:
            Dictionary mapping metric names to metadata list

        """
        params: dict[str, Any] = {}
        if metric:
            params["metric"] = metric

        response = await self._make_request(
            method="GET",
            endpoint="prometheus/api/v1/metadata",
            params=params,
        )

        # Response format: {"status": "success", "data": {"metric_name": [{"type": "...", "help": "...", ...}]}}
        if response.get("status") == "success":
            return response.get("data", {})

        return {}

    async def get_metric_labels(self, metric_name: str | None = None) -> list[str]:
        """Get label names for metrics.

        Args:
            metric_name: Optional metric name to filter labels

        Returns:
            List of label names

        """
        params: dict[str, Any] = {}
        if metric_name:
            # Use a query to get labels for specific metric
            params["match[]"] = f"{{{metric_name}=~'.+'}}"

        response = await self._make_request(
            method="GET",
            endpoint="prometheus/api/v1/labels",
            params=params,
        )

        # Response format: {"status": "success", "data": ["label1", "label2", ...]}
        if response.get("status") == "success":
            return response.get("data", [])

        return []

    async def get_label_values(
        self,
        label_name: str,
        match: list[str] | None = None,
    ) -> list[str]:
        """Get values for a specific label.

        Args:
            label_name: Label name to get values for
            match: Optional list of series selectors to filter values

        Returns:
            List of label values

        """
        params: dict[str, Any] = {}
        if match:
            params["match[]"] = match

        response = await self._make_request(
            method="GET",
            endpoint=f"prometheus/api/v1/label/{label_name}/values",
            params=params,
        )

        # Response format: {"status": "success", "data": ["value1", "value2", ...]}
        if response.get("status") == "success":
            return response.get("data", [])

        return []


# 🧱🏗️🔚
