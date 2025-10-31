#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Search operations for OpenObserve."""

from __future__ import annotations

import re

from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.models import SearchResponse
from provide.foundation.logger import get_logger

log = get_logger(__name__)


def _sanitize_stream_name(stream: str) -> str:
    """Sanitize stream name to prevent SQL injection."""
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")
    return stream


def _sanitize_trace_id(trace_id: str) -> str:
    """Sanitize trace ID to prevent SQL injection."""
    # Allow hex strings and UUID format (with hyphens)
    if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
        raise ValueError(f"Invalid trace_id format: {trace_id}")
    return trace_id


def _sanitize_log_level(level: str) -> str:
    """Sanitize log level to prevent SQL injection."""
    from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

    if level not in _VALID_LOG_LEVEL_TUPLE:
        raise ValueError(f"Invalid log level: {level}")
    return level


def _sanitize_service_name(service: str) -> str:
    """Sanitize service name to prevent SQL injection."""
    if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
        raise ValueError(f"Invalid service name: {service}")
    return service


async def search_logs(
    sql: str,
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    size: int = 100,
    client: OpenObserveClient | None = None,
) -> SearchResponse:
    """Search logs in OpenObserve.

    Args:
        sql: SQL query to execute
        start_time: Start time (relative like "-1h" or microseconds)
        end_time: End time (relative like "now" or microseconds)
        size: Number of results to return
        client: OpenObserve client (creates new if not provided)

    Returns:
        SearchResponse with results

    """
    if client is None:
        client = OpenObserveClient.from_config()

    return await client.search(
        sql=sql,
        start_time=start_time,
        end_time=end_time,
        size=size,
    )


async def search_by_trace_id(
    trace_id: str,
    stream: str = "default",
    client: OpenObserveClient | None = None,
) -> SearchResponse:
    """Search for logs by trace ID.

    Args:
        trace_id: Trace ID to search for
        stream: Stream name to search in
        client: OpenObserve client (creates new if not provided)

    Returns:
        SearchResponse with matching logs

    """
    # Sanitize inputs to prevent SQL injection
    safe_stream = _sanitize_stream_name(stream)
    safe_trace_id = _sanitize_trace_id(trace_id)
    sql = f"SELECT * FROM {safe_stream} WHERE trace_id = '{safe_trace_id}' ORDER BY _timestamp ASC"  # nosec B608 - Inputs sanitized via _sanitize_* functions
    return await search_logs(sql=sql, start_time="-24h", client=client)


async def search_by_level(
    level: str,
    stream: str = "default",
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    size: int = 100,
    client: OpenObserveClient | None = None,
) -> SearchResponse:
    """Search for logs by level.

    Args:
        level: Log level to filter (ERROR, WARN, INFO, DEBUG, etc.)
        stream: Stream name to search in
        start_time: Start time
        end_time: End time
        size: Number of results
        client: OpenObserve client

    Returns:
        SearchResponse with matching logs

    """
    # Sanitize inputs to prevent SQL injection
    safe_stream = _sanitize_stream_name(stream)
    safe_level = _sanitize_log_level(level)
    sql = f"SELECT * FROM {safe_stream} WHERE level = '{safe_level}' ORDER BY _timestamp DESC"  # nosec B608 - Inputs sanitized via _sanitize_* functions
    return await search_logs(
        sql=sql,
        start_time=start_time,
        end_time=end_time,
        size=size,
        client=client,
    )


async def search_errors(
    stream: str = "default",
    start_time: str | int | None = None,
    size: int = 100,
    client: OpenObserveClient | None = None,
) -> SearchResponse:
    """Search for error logs.

    Args:
        stream: Stream name to search in
        start_time: Start time
        size: Number of results
        client: OpenObserve client

    Returns:
        SearchResponse with error logs

    """
    return await search_by_level(
        level="ERROR",
        stream=stream,
        start_time=start_time,
        size=size,
        client=client,
    )


async def search_by_service(
    service: str,
    stream: str = "default",
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    size: int = 100,
    client: OpenObserveClient | None = None,
) -> SearchResponse:
    """Search for logs by service name.

    Args:
        service: Service name to filter
        stream: Stream name to search in
        start_time: Start time
        end_time: End time
        size: Number of results
        client: OpenObserve client

    Returns:
        SearchResponse with matching logs

    """
    # Sanitize inputs to prevent SQL injection
    safe_stream = _sanitize_stream_name(stream)
    safe_service = _sanitize_service_name(service)
    sql = f"SELECT * FROM {safe_stream} WHERE service_name = '{safe_service}' ORDER BY _timestamp DESC"  # nosec B608 - Inputs sanitized via _sanitize_* functions
    return await search_logs(
        sql=sql,
        start_time=start_time,
        end_time=end_time,
        size=size,
        client=client,
    )


async def aggregate_by_level(
    stream: str = "default",
    start_time: str | int | None = None,
    end_time: str | int | None = None,
    client: OpenObserveClient | None = None,
) -> dict[str, int]:
    """Get count of logs by level.

    Args:
        stream: Stream name to search in
        start_time: Start time
        end_time: End time
        client: OpenObserve client

    Returns:
        Dictionary mapping level to count

    """
    # Sanitize stream name to prevent SQL injection
    safe_stream = _sanitize_stream_name(stream)
    sql = f"SELECT level, COUNT(*) as count FROM {safe_stream} GROUP BY level"  # nosec B608 - Inputs sanitized via _sanitize_* functions
    response = await search_logs(
        sql=sql,
        start_time=start_time,
        end_time=end_time,
        size=1000,
        client=client,
    )

    result = {}
    for hit in response.hits:
        level = hit.get("level", "UNKNOWN")
        count = hit.get("count", 0)
        result[level] = count

    return result


async def get_current_trace_logs(
    stream: str = "default",
    client: OpenObserveClient | None = None,
) -> SearchResponse | None:
    """Get logs for the current active trace.

    Args:
        stream: Stream name to search in
        client: OpenObserve client

    Returns:
        SearchResponse with logs for current trace, or None if no active trace

    """
    # Try to get current trace ID from OpenTelemetry
    try:
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            trace_id = f"{span_context.trace_id:032x}"
            return await search_by_trace_id(trace_id, stream=stream, client=client)
    except ImportError:
        pass

    # Try to get from Foundation tracer
    try:
        from provide.foundation.tracer.context import get_current_trace_id

        trace_id = get_current_trace_id()  # type: ignore[assignment]
        if trace_id:
            return await search_by_trace_id(trace_id, stream=stream, client=client)
    except ImportError:
        pass

    return None


# 🧱🏗️🔚
