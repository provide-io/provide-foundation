"""
Search operations for OpenObserve.
"""


from provide.foundation.logger import get_logger
from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.models import SearchResponse

log = get_logger(__name__)


def search_logs(
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

    return client.search(
        sql=sql,
        start_time=start_time,
        end_time=end_time,
        size=size,
    )


def search_by_trace_id(
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
    sql = (
        f"SELECT * FROM {stream} WHERE trace_id = '{trace_id}' ORDER BY _timestamp ASC"
    )
    return search_logs(sql=sql, start_time="-24h", client=client)


def search_by_level(
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
    sql = f"SELECT * FROM {stream} WHERE level = '{level}' ORDER BY _timestamp DESC"
    return search_logs(
        sql=sql,
        start_time=start_time,
        end_time=end_time,
        size=size,
        client=client,
    )


def search_errors(
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
    return search_by_level(
        level="ERROR",
        stream=stream,
        start_time=start_time,
        size=size,
        client=client,
    )


def search_by_service(
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
    sql = f"SELECT * FROM {stream} WHERE service = '{service}' ORDER BY _timestamp DESC"
    return search_logs(
        sql=sql,
        start_time=start_time,
        end_time=end_time,
        size=size,
        client=client,
    )


def aggregate_by_level(
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
    sql = f"SELECT level, COUNT(*) as count FROM {stream} GROUP BY level"
    response = search_logs(
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


def get_current_trace_logs(
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
            return search_by_trace_id(trace_id, stream=stream, client=client)
    except ImportError:
        pass

    # Try to get from Foundation tracer
    try:
        from provide.foundation.tracer.context import get_current_trace_id

        trace_id = get_current_trace_id()
        if trace_id:
            return search_by_trace_id(trace_id, stream=stream, client=client)
    except ImportError:
        pass

    return None
