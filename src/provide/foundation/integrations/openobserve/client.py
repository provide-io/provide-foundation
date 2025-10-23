# provide/foundation/integrations/openobserve/client.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""OpenObserve API client using Foundation's transport system."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from urllib.parse import urljoin

from provide.foundation.errors.decorators import resilient
from provide.foundation.hub import get_hub
from provide.foundation.integrations.openobserve.auth import (
    get_auth_headers,
    validate_credentials,
)
from provide.foundation.integrations.openobserve.exceptions import (
    OpenObserveConfigError,
    OpenObserveConnectionError,
    OpenObserveQueryError,
)
from provide.foundation.integrations.openobserve.models import (
    SearchQuery,
    SearchResponse,
    StreamInfo,
    parse_relative_time,
)
from provide.foundation.logger import get_logger
from provide.foundation.transport import UniversalClient
from provide.foundation.transport.errors import (
    TransportConnectionError,
    TransportError,
    TransportTimeoutError,
)

log = get_logger(__name__)


class OpenObserveClient:
    """Async client for interacting with OpenObserve API.

    Uses Foundation's transport system for all HTTP operations.
    """

    def __init__(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
    ) -> None:
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds

        Note:
            Retry logic is handled automatically by UniversalClient's middleware.

        """
        self.url = url.rstrip("/")
        self.username, self.password = validate_credentials(username, password)
        self.organization = organization

        # Create UniversalClient with auth headers and timeout
        self._client = UniversalClient(
            hub=get_hub(),
            default_headers=get_auth_headers(self.username, self.password),
            default_timeout=float(timeout),
        )

    @classmethod
    def from_config(cls) -> OpenObserveClient:
        """Create client from OpenObserveConfig.

        Returns:
            Configured OpenObserveClient instance

        Raises:
            OpenObserveConfigError: If configuration is missing

        """
        from provide.foundation.integrations.openobserve.config import OpenObserveConfig

        config = OpenObserveConfig.from_env()

        if not config.url:
            raise OpenObserveConfigError(
                "OpenObserve URL not configured. Set OPENOBSERVE_URL environment variable.",
            )

        if not config.user or not config.password:
            raise OpenObserveConfigError(
                "OpenObserve credentials not configured. "
                "Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables.",
            )

        return cls(
            url=config.url,
            username=config.user,
            password=config.password,
            organization=config.org or "default",
        )

    def _extract_error_message(self, response: Any, default_msg: str) -> str:
        """Extract error message from response.

        Args:
            response: Response object
            default_msg: Default message if extraction fails

        Returns:
            Error message string

        """
        try:
            error_data = response.json()
            if isinstance(error_data, dict) and "message" in error_data:
                return error_data["message"]
        except Exception:
            pass
        return default_msg

    def _check_response_errors(self, response: Any) -> None:
        """Check response for errors and raise appropriate exceptions.

        Args:
            response: Response object to check

        Raises:
            OpenObserveConnectionError: On authentication errors
            OpenObserveQueryError: On HTTP errors

        """
        if response.status == 401:
            raise OpenObserveConnectionError("Authentication failed. Check credentials.")

        if not response.is_success():
            error_msg = self._extract_error_message(response, f"HTTP {response.status} error")
            raise OpenObserveQueryError(f"API error: {error_msg}")

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request to OpenObserve API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response data as dictionary

        Raises:
            OpenObserveConnectionError: On connection errors
            OpenObserveQueryError: On API errors

        """
        uri = urljoin(self.url, f"/api/{self.organization}/{endpoint}")

        try:
            response = await self._client.request(
                uri=uri,
                method=method,
                params=params,
                body=json_data,
            )

            self._check_response_errors(response)

            # Handle empty responses
            if not response.body:
                return {}

            return response.json()

        except TransportConnectionError as e:
            raise OpenObserveConnectionError(f"Failed to connect to OpenObserve: {e}") from e
        except TransportTimeoutError as e:
            raise OpenObserveConnectionError(f"Request timed out: {e}") from e
        except TransportError as e:
            raise OpenObserveQueryError(f"Transport error: {e}") from e
        except (OpenObserveConnectionError, OpenObserveQueryError):
            raise
        except Exception as e:
            raise OpenObserveQueryError(f"Unexpected error: {e}") from e

    async def search(
        self,
        sql: str,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
        size: int = 100,
        from_offset: int = 0,
    ) -> SearchResponse:
        """Execute a search query.

        Args:
            sql: SQL query to execute
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)
            size: Number of results to return
            from_offset: Offset for pagination

        Returns:
            SearchResponse with results

        """
        # Parse time parameters
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        # Create query
        query = SearchQuery(
            sql=sql,
            start_time=start_ts,
            end_time=end_ts,
            size=size,
            from_offset=from_offset,
        )

        log.debug(f"Executing search query: {sql}")

        # Make request
        response = await self._make_request(
            method="POST",
            endpoint="_search",
            params={"is_ui_histogram": "false", "is_multi_stream_search": "false"},
            json_data=query.to_dict(),
        )

        # Handle errors in response
        if "error" in response:
            raise OpenObserveQueryError(f"Query error: {response['error']}")

        result = SearchResponse.from_dict(response)

        # Log any function errors
        if result.function_error:
            for error in result.function_error:
                log.warning(f"Query warning: {error}")

        log.info(f"Search completed: {len(result.hits)} hits, took {result.took}ms")

        return result

    async def list_streams(self) -> list[StreamInfo]:
        """List available streams.

        Returns:
            List of StreamInfo objects

        """
        response = await self._make_request(
            method="GET",
            endpoint="streams",
        )

        streams = []
        if isinstance(response, dict):
            # Response is a dict of stream types to stream lists
            for _stream_type, stream_list in response.items():
                if isinstance(stream_list, list):
                    for stream_data in stream_list:
                        if isinstance(stream_data, dict):
                            stream_info = StreamInfo.from_dict(stream_data)
                            streams.append(stream_info)

        return streams

    async def get_search_history(
        self,
        stream_name: str | None = None,
        size: int = 100,
        start_time: str | int | None = None,
        end_time: str | int | None = None,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return
            start_time: Start time (relative like "-1h" or microseconds)
            end_time: End time (relative like "now" or microseconds)

        Returns:
            SearchResponse with history entries

        """
        # Parse time parameters (default to last hour if not specified)
        now = datetime.now()

        if start_time is None:
            start_time = "-1h"
        if end_time is None:
            end_time = "now"

        start_ts = parse_relative_time(str(start_time), now) if isinstance(start_time, str) else start_time
        end_ts = parse_relative_time(str(end_time), now) if isinstance(end_time, str) else end_time

        request_data: dict[str, Any] = {
            "size": size,
            "start_time": start_ts,
            "end_time": end_ts,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = await self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    @resilient(
        fallback=False,
        suppress=(Exception,),
        reraise=False,
        context={"method": "test_connection"},
    )
    async def test_connection(self) -> bool:
        """Test connection to OpenObserve.

        Uses the @resilient decorator for standardized error handling and logging.

        Returns:
            True if connection successful, False otherwise

        """
        # Try to list streams as a simple test
        await self.list_streams()
        return True

    # Metrics API Methods (Prometheus-compatible)

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


# <3 🧱🤝🔌🪄
