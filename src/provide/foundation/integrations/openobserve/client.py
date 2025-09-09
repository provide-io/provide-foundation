"""
OpenObserve API client.
"""

from datetime import datetime
import json
from typing import Any
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from provide.foundation.logger import get_logger
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

log = get_logger(__name__)


class OpenObserveClient:
    """Client for interacting with OpenObserve API."""

    def __init__(
        self,
        url: str,
        username: str,
        password: str,
        organization: str = "default",
        timeout: int = 30,
        max_retries: int = 3,
    ):
        """Initialize OpenObserve client.

        Args:
            url: Base URL for OpenObserve API
            username: Username for authentication
            password: Password for authentication
            organization: Organization name (default: "default")
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.url = url.rstrip("/")
        self.username, self.password = validate_credentials(username, password)
        self.organization = organization
        self.timeout = timeout

        # Setup session with retry logic
        self.session = requests.Session()
        retry = Retry(
            total=max_retries,
            backoff_factor=0.3,
            status_forcelist=[500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Set default headers
        self.session.headers.update(get_auth_headers(self.username, self.password))

    @classmethod
    def from_config(cls) -> "OpenObserveClient":
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
                "OpenObserve URL not configured. Set OPENOBSERVE_URL environment variable."
            )

        if not config.user or not config.password:
            raise OpenObserveConfigError(
                "OpenObserve credentials not configured. "
                "Set OPENOBSERVE_USER and OPENOBSERVE_PASSWORD environment variables."
            )

        return cls(
            url=config.url,
            username=config.user,
            password=config.password,
            organization=config.org or "default",
        )

    def _make_request(
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
        url = urljoin(self.url, f"/api/{self.organization}/{endpoint}")

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                timeout=self.timeout,
            )

            if response.status_code == 401:
                raise OpenObserveConnectionError(
                    "Authentication failed. Check credentials."
                )

            response.raise_for_status()

            # Handle empty responses
            if not response.content:
                return {}

            return response.json()

        except requests.exceptions.ConnectionError as e:
            raise OpenObserveConnectionError(f"Failed to connect to OpenObserve: {e}")
        except requests.exceptions.Timeout as e:
            raise OpenObserveConnectionError(f"Request timed out: {e}")
        except requests.exceptions.HTTPError as e:
            # Try to extract error message from response
            error_msg = str(e)
            try:
                error_data = e.response.json()
                if "message" in error_data:
                    error_msg = error_data["message"]
            except (json.JSONDecodeError, AttributeError):
                pass
            raise OpenObserveQueryError(f"API error: {error_msg}")
        except Exception as e:
            raise OpenObserveQueryError(f"Unexpected error: {e}")

    def search(
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

        start_ts = (
            parse_relative_time(str(start_time), now)
            if isinstance(start_time, str)
            else start_time
        )
        end_ts = (
            parse_relative_time(str(end_time), now)
            if isinstance(end_time, str)
            else end_time
        )

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
        response = self._make_request(
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

    def list_streams(self) -> list[StreamInfo]:
        """List available streams.

        Returns:
            List of StreamInfo objects
        """
        response = self._make_request(
            method="GET",
            endpoint="streams",
        )

        streams = []
        if isinstance(response, dict):
            # Response is a dict of stream types to stream lists
            for stream_type, stream_list in response.items():
                if isinstance(stream_list, list):
                    for stream_data in stream_list:
                        if isinstance(stream_data, dict):
                            stream_info = StreamInfo.from_dict(stream_data)
                            streams.append(stream_info)

        return streams

    def get_search_history(
        self,
        stream_name: str | None = None,
        size: int = 100,
    ) -> SearchResponse:
        """Get search history.

        Args:
            stream_name: Filter by stream name
            size: Number of history entries to return

        Returns:
            SearchResponse with history entries
        """
        request_data = {
            "size": size,
        }

        if stream_name:
            request_data["stream_name"] = stream_name

        response = self._make_request(
            method="POST",
            endpoint="_search_history",
            json_data=request_data,
        )

        return SearchResponse.from_dict(response)

    def test_connection(self) -> bool:
        """Test connection to OpenObserve.

        Returns:
            True if connection successful
        """
        try:
            # Try to list streams as a simple test
            self.list_streams()
            return True
        except Exception as e:
            log.error(f"Connection test failed: {e}")
            return False
