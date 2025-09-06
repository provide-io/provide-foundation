"""
OpenObserve integration for Foundation.

Provides log querying and streaming capabilities when OpenTelemetry is available.
"""

from provide.foundation.observability.openobserve.client import OpenObserveClient
from provide.foundation.observability.openobserve.exceptions import (
    OpenObserveAuthenticationError,
    OpenObserveConfigError,
    OpenObserveConnectionError,
    OpenObserveError,
    OpenObserveQueryError,
    OpenObserveStreamingError,
)
from provide.foundation.observability.openobserve.formatters import (
    format_csv,
    format_json,
    format_log_line,
    format_output,
    format_summary,
    format_table,
)
from provide.foundation.observability.openobserve.models import (
    SearchQuery,
    SearchResponse,
    StreamInfo,
    parse_relative_time,
)
from provide.foundation.observability.openobserve.search import (
    aggregate_by_level,
    get_current_trace_logs,
    search_by_level,
    search_by_service,
    search_by_trace_id,
    search_errors,
    search_logs,
)
from provide.foundation.observability.openobserve.streaming import (
    stream_logs,
    stream_search_http2,
    tail_logs,
)

__all__ = [
    # Client
    "OpenObserveClient",
    # Search functions
    "search_logs",
    "search_by_trace_id",
    "search_by_level",
    "search_errors",
    "search_by_service",
    "aggregate_by_level",
    "get_current_trace_logs",
    # Streaming functions
    "stream_logs",
    "stream_search_http2",
    "tail_logs",
    # Models
    "SearchQuery",
    "SearchResponse",
    "StreamInfo",
    "parse_relative_time",
    # Formatters
    "format_json",
    "format_log_line",
    "format_table",
    "format_csv",
    "format_summary",
    "format_output",
    # Exceptions
    "OpenObserveError",
    "OpenObserveConnectionError",
    "OpenObserveAuthenticationError",
    "OpenObserveQueryError",
    "OpenObserveStreamingError",
    "OpenObserveConfigError",
]
