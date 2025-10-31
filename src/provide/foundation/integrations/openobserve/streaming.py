#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Streaming search operations for OpenObserve using Foundation transport."""

from __future__ import annotations

from collections.abc import AsyncGenerator, Generator
import re
import time
from typing import Any

from provide.foundation.console.output import perr
from provide.foundation.errors import ValidationError
from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.exceptions import (
    OpenObserveStreamingError,
)
from provide.foundation.integrations.openobserve.models import parse_relative_time
from provide.foundation.serialization import json_dumps, json_loads
from provide.foundation.utils.async_helpers import run_async


def stream_logs(
    sql: str,
    start_time: str | int | None = None,
    poll_interval: int = 5,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream logs from OpenObserve with polling.

    Continuously polls for new logs and yields them as they arrive.

    Args:
        sql: SQL query to execute
        start_time: Initial start time
        poll_interval: Seconds between polls
        client: OpenObserve client

    Yields:
        Log entries as they arrive

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Track the last seen timestamp to avoid duplicates
    if start_time is None:
        last_timestamp = parse_relative_time("-1m")
    elif isinstance(start_time, str):
        last_timestamp = parse_relative_time(start_time)
    else:
        # Already an int (microseconds)
        last_timestamp = start_time
    seen_ids = set()

    while True:
        try:
            # Search for new logs since last timestamp using async client
            response = run_async(
                client.search(
                    sql=sql,
                    start_time=last_timestamp,
                    end_time="now",
                    size=1000,
                )
            )

            # Process new logs
            for hit in response.hits:
                # Create a unique ID for deduplication
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json_dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = timestamp + 1  # Add 1 microsecond to avoid duplicates

            # Clean up old seen IDs to prevent memory growth
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            perr(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}") from e


def _parse_time_param(time_param: str | int | None, default: str) -> int:
    """Parse time parameter to microseconds."""
    if time_param is None:
        return parse_relative_time(default)
    if isinstance(time_param, str):
        return parse_relative_time(time_param)
    return time_param


def _process_stream_line(line: str) -> list[dict[str, Any]]:
    """Process a single line from stream response."""
    if not line:
        return []

    try:
        parsed_data = json_loads(line)
        if isinstance(parsed_data, dict):
            if "hits" in parsed_data:
                return parsed_data["hits"]
            return [parsed_data]
    except Exception:
        pass

    return []


async def stream_search_http2_async(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream search results using HTTP/2 streaming endpoint (async version).

    Uses Foundation's transport for HTTP/2 streaming.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """
    if client is None:
        client = OpenObserveClient.from_config()

    # Parse times
    start_ts = _parse_time_param(start_time, "-1h")
    end_ts = _parse_time_param(end_time, "now")

    # Prepare request
    uri = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    try:
        # Use Foundation's transport for streaming
        async for chunk in client._client.stream(uri=uri, method="POST", params=params, body=data):
            # Decode chunk and process lines
            lines = chunk.decode("utf-8").strip().split("\n")
            for line in lines:
                for hit in _process_stream_line(line):
                    yield hit

    except Exception as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}") from e


def stream_search_http2(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream search results using HTTP/2 streaming endpoint (sync wrapper).

    This is a sync wrapper around the async streaming function for CLI use.

    Args:
        sql: SQL query to execute
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Yields:
        Log entries as they stream

    """

    async def _stream() -> list[dict[str, Any]]:
        results = []
        async for item in stream_search_http2_async(
            sql=sql, start_time=start_time, end_time=end_time, client=client
        ):
            results.append(item)
        return results

    results = run_async(_stream())
    yield from results


def _build_where_clause_from_filters(filters: dict[str, str]) -> str:
    """Safely build a SQL WHERE clause from a dictionary of filters."""
    if not filters:
        return ""

    conditions = []
    for key, value in filters.items():
        # Sanitize column name (key)
        if not re.match(r"^[a-zA-Z0-9_]+$", key):
            raise ValidationError(f"Invalid filter key: {key}")

        # Escape single quotes in value
        escaped_value = value.replace("'", "''")
        conditions.append(f"{key} = '{escaped_value}'")

    return f"WHERE {' AND '.join(conditions)}"


def tail_logs(
    stream: str = "default",
    filters: dict[str, str] | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filters: Dictionary of key-value pairs for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries

    """
    # Sanitize stream name to prevent SQL injection
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValidationError(
            "Invalid stream name", code="INVALID_STREAM_NAME", stream=stream, allowed_pattern="^[a-zA-Z0-9_]+$"
        )

    # Validate lines parameter
    if not isinstance(lines, int) or lines <= 0 or lines > 10000:
        raise ValidationError(
            "Invalid lines parameter", code="INVALID_LINES_PARAM", lines=lines, expected_range="1-10000"
        )

    # Build WHERE clause safely from filters
    where_clause = _build_where_clause_from_filters(filters or {})
    sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs using async client
    response = run_async(client.search(sql=sql, start_time="-1h"))

    # Yield initial logs in reverse order (oldest first)
    yield from reversed(response.hits)

    # If follow mode, continue streaming
    if follow:
        # Get the latest timestamp from initial results
        if response.hits:
            last_timestamp = max(hit.get("_timestamp", 0) for hit in response.hits)
        else:
            last_timestamp = parse_relative_time("-1s")

        # Build streaming query
        stream_sql = f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp ASC"

        # Stream new logs
        yield from stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        )


# 🧱🏗️🔚
