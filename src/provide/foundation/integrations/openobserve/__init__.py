#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.config import OpenObserveConfig
from provide.foundation.integrations.openobserve.exceptions import (
    OpenObserveAuthenticationError,
    OpenObserveConfigError,
    OpenObserveConnectionError,
    OpenObserveError,
    OpenObserveQueryError,
    OpenObserveStreamingError,
)
from provide.foundation.integrations.openobserve.formatters import (
    format_csv,
    format_json,
    format_log_line,
    format_output,
    format_summary,
    format_table,
)
from provide.foundation.integrations.openobserve.models import (
    SearchQuery,
    SearchResponse,
    StreamInfo,
    parse_relative_time,
)
from provide.foundation.integrations.openobserve.search import (
    aggregate_by_level,
    get_current_trace_logs,
    search_by_level,
    search_by_service,
    search_by_trace_id,
    search_errors,
    search_logs,
)
from provide.foundation.integrations.openobserve.streaming import (
    stream_logs,
    stream_search_http2,
    tail_logs,
)

# Metrics support
try:
    from provide.foundation.integrations.openobserve.metrics_formatters import (
        format_metric_output,
        format_metrics_list,
    )
    from provide.foundation.integrations.openobserve.metrics_models import (
        MetricMetadata,
        MetricQueryResult,
        MetricSample,
    )

    _HAS_METRICS = True
except ImportError:
    _HAS_METRICS = False
    MetricMetadata = None  # type: ignore[assignment, misc]
    MetricQueryResult = None  # type: ignore[assignment, misc]
    MetricSample = None  # type: ignore[assignment, misc]
    format_metric_output = None  # type: ignore[assignment]
    format_metrics_list = None  # type: ignore[assignment]

"""OpenObserve integration for Foundation.

Provides log querying, streaming, and metrics capabilities as an optional integration.
"""

__all__ = [
    # Metrics (if available)
    "MetricMetadata",
    "MetricQueryResult",
    "MetricSample",
    "OpenObserveAuthenticationError",
    # Client
    "OpenObserveClient",
    # Configuration
    "OpenObserveConfig",
    "OpenObserveConfigError",
    "OpenObserveConnectionError",
    # Exceptions
    "OpenObserveError",
    "OpenObserveQueryError",
    "OpenObserveStreamingError",
    # Models
    "SearchQuery",
    "SearchResponse",
    "StreamInfo",
    "aggregate_by_level",
    "format_csv",
    # Formatters
    "format_json",
    "format_log_line",
    "format_metric_output",
    "format_metrics_list",
    "format_output",
    "format_summary",
    "format_table",
    "get_current_trace_logs",
    "parse_relative_time",
    "search_by_level",
    "search_by_service",
    "search_by_trace_id",
    "search_errors",
    # Search functions
    "search_logs",
    # Streaming functions
    "stream_logs",
    "stream_search_http2",
    "tail_logs",
]

# 🧱🏗️🔚
