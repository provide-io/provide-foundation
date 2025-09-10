"""
Streaming search operations for OpenObserve.
"""

from collections.abc import Generator
import json
import time
from typing import Any

import requests

from provide.foundation.logger import get_logger
from provide.foundation.integrations.openobserve.auth import get_auth_headers
from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.exceptions import (
    OpenObserveStreamingError,
)
from provide.foundation.integrations.openobserve.models import parse_relative_time

log = get_logger(__name__)


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
    last_timestamp = (
        parse_relative_time(start_time) if start_time else parse_relative_time("-1m")
    )
    seen_ids = set()

    log.info(f"Starting log stream with query: {sql}")

    while True:
        try:
            # Search for new logs since last timestamp
            response = client.search(
                sql=sql,
                start_time=last_timestamp,
                end_time="now",
                size=1000,
            )

            # Process new logs
            new_count = 0
            for hit in response.hits:
                # Create a unique ID for deduplication
                # Use combination of timestamp and a hash of content
                timestamp = hit.get("_timestamp", 0)
                log_id = f"{timestamp}:{hash(json.dumps(hit, sort_keys=True))}"

                if log_id not in seen_ids:
                    seen_ids.add(log_id)
                    new_count += 1
                    yield hit

                    # Update last timestamp
                    if timestamp > last_timestamp:
                        last_timestamp = (
                            timestamp + 1
                        )  # Add 1 microsecond to avoid duplicates

            if new_count > 0:
                log.debug(f"Streamed {new_count} new log entries")

            # Clean up old seen IDs to prevent memory growth
            # Keep only IDs from the last minute
            cutoff_time = parse_relative_time("-1m")
            seen_ids = {lid for lid in seen_ids if int(lid.split(":")[0]) > cutoff_time}

            # Wait before next poll
            time.sleep(poll_interval)

        except KeyboardInterrupt:
            log.info("Stream interrupted by user")
            break
        except Exception as e:
            log.error(f"Error during streaming: {e}")
            raise OpenObserveStreamingError(f"Streaming failed: {e}")


def stream_search_http2(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Stream search results using HTTP/2 streaming endpoint.

    This uses the native HTTP/2 streaming capability of OpenObserve
    for real-time log streaming.

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
    start_ts = (
        parse_relative_time(start_time) if start_time else parse_relative_time("-1h")
    )
    end_ts = parse_relative_time(end_time) if end_time else parse_relative_time("now")

    # Prepare request
    url = f"{client.url}/api/{client.organization}/_search_stream"
    params = {
        "is_ui_histogram": "false",
        "is_multi_stream_search": "false",
    }
    data = {
        "sql": sql,
        "start_time": start_ts,
        "end_time": end_ts,
    }

    headers = get_auth_headers(client.username, client.password)

    log.info(f"Starting HTTP/2 stream with query: {sql}")

    try:
        # Make streaming request
        with requests.post(
            url,
            params=params,
            json=data,
            headers=headers,
            stream=True,
            timeout=client.timeout,
        ) as response:
            response.raise_for_status()

            # Process streaming response
            for line in response.iter_lines():
                if line:
                    try:
                        # Decode and parse JSON line
                        data = json.loads(line.decode("utf-8"))

                        # Handle different response formats
                        if isinstance(data, dict):
                            if "hits" in data:
                                # Batch of results
                                for hit in data["hits"]:
                                    yield hit
                            else:
                                # Single result
                                yield data
                    except json.JSONDecodeError as e:
                        log.warning(f"Failed to parse stream line: {e}")
                        continue

    except requests.exceptions.RequestException as e:
        raise OpenObserveStreamingError(f"HTTP/2 streaming failed: {e}")


def tail_logs(
    stream: str = "default",
    filter_sql: str | None = None,
    follow: bool = True,
    lines: int = 10,
    client: OpenObserveClient | None = None,
) -> Generator[dict[str, Any], None, None]:
    """Tail logs similar to 'tail -f' command.

    Args:
        stream: Stream name to tail
        filter_sql: Optional SQL WHERE clause for filtering
        follow: If True, continue streaming new logs
        lines: Number of initial lines to show
        client: OpenObserve client

    Yields:
        Log entries
    """
    # Build SQL query
    where_clause = f"WHERE {filter_sql}" if filter_sql else ""
    sql = (
        f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {lines}"
    )

    if client is None:
        client = OpenObserveClient.from_config()

    # Get initial logs
    log.info(f"Fetching last {lines} logs from {stream}")
    response = client.search(sql=sql, start_time="-1h")

    # Yield initial logs in reverse order (oldest first)
    for hit in reversed(response.hits):
        yield hit

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
        for log_entry in stream_logs(
            sql=stream_sql,
            start_time=last_timestamp + 1,
            client=client,
        ):
            yield log_entry
