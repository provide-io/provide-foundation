#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Search and streams operations for OpenObserve client."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from provide.foundation.errors.decorators import resilient
from provide.foundation.integrations.openobserve.exceptions import OpenObserveQueryError
from provide.foundation.integrations.openobserve.models import (
    SearchQuery,
    SearchResponse,
    StreamInfo,
    parse_relative_time,
)
from provide.foundation.logger import get_logger

log = get_logger(__name__)


class SearchOperationsMixin:
    """Mixin providing search and streams operations."""

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


# 🧱🏗️🔚
